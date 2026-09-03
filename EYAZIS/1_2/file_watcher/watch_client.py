#!/usr/bin/env python3
"""
File watcher client for the EYAZIS/1_2 IR system.

Monitors a local directory with `watchdog` and pushes file change events
to the IR server, which re-indexes the affected documents.

On startup, compares the current filesystem state against a saved state
file (.watch_state.json) and sends only new/changed/deleted files — no
need to pass --init on every run.

Usage:
    python watch_client.py /path/to/dir
    python watch_client.py /path/to/dir --server http://192.168.1.100:5000
    python watch_client.py /path/to/dir --recursive --ext .txt,.pdf,.docx

Requires: pip install -r requirements.txt
"""
import argparse
import base64
import json
import os
import sys
import time

import requests
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

DEFAULT_EXTENSIONS = [".txt", ".md", ".pdf", ".docx", ".html", ".rtf", ".csv", ".log"]
DEFAULT_STATE_FILE = ".watch_state.json"


class WatchState:
    """Persists {filepath: {mtime, size}} to detect new/changed/deleted files."""

    def __init__(self, path):
        self.path = path
        self.files = {}
        self._load()

    def _load(self):
        if not os.path.isfile(self.path):
            return
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
            self.files = data.get("files", {})
        except (json.JSONDecodeError, OSError):
            self.files = {}

    def save(self):
        try:
            with open(self.path, "w") as f:
                json.dump({"files": self.files}, f, indent=2)
        except OSError as exc:
            print(f"[state] cannot save {self.path}: {exc}", file=sys.stderr)

    def update(self, filepath, mtime, size):
        self.files[filepath] = {"mtime": mtime, "size": size}

    def remove(self, filepath):
        self.files.pop(filepath, None)

    def get(self, filepath):
        return self.files.get(filepath)


class WatchEventHandler(FileSystemEventHandler):
    def __init__(self, server_url, client_id, extensions, state, debounce=2.0):
        self.server_url = server_url
        self.client_id = client_id
        self.extensions = set(extensions)
        self.state = state
        self.debounce = debounce
        self._last_sent = {}

    def _relevant(self, path):
        return os.path.splitext(path)[1].lower() in self.extensions

    def _debounced(self, path):
        now = time.time()
        last = self._last_sent.get(path, 0.0)
        if now - last < self.debounce:
            return True
        self._last_sent[path] = now
        return False

    def _send(self, event_type, src_path, old_path=None):
        if not self._relevant(src_path):
            return
        if self._debounced(src_path):
            return

        abs_path = os.path.abspath(src_path)
        payload = {
            "event_type": event_type,
            "file_path": abs_path,
            "client_id": self.client_id,
        }
        if old_path:
            payload["old_path"] = os.path.abspath(old_path)

        if event_type in ("created", "modified"):
            try:
                with open(src_path, "rb") as fh:
                    payload["file_content"] = base64.b64encode(fh.read()).decode("utf-8")
            except OSError as exc:
                print(f"[watch] cannot read {src_path}: {exc}", file=sys.stderr)
                return

        try:
            resp = requests.post(f"{self.server_url}/api/watch-event", json=payload, timeout=10)
            if resp.status_code in (200, 201):
                self._update_state(event_type, abs_path)
            else:
                print(f"[watch] {event_type} {src_path} -> HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
        except requests.RequestException as exc:
            print(f"[watch] failed to notify server: {exc}", file=sys.stderr)

    def _update_state(self, event_type, abs_path):
        if event_type in ("created", "modified"):
            try:
                st = os.stat(abs_path)
                self.state.update(abs_path, st.st_mtime, st.st_size)
            except OSError:
                pass
        elif event_type == "deleted":
            self.state.remove(abs_path)
        self.state.save()

    def on_created(self, event):
        if not event.is_directory:
            self._send("created", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._send("modified", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self._send("deleted", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._send("deleted", event.src_path)
            self._send("created", event.dest_path)


def _scan_directory(watch_dir, extensions, recursive):
    """Walk directory and return {abs_path: {mtime, size}} for matching files."""
    ext_set = set(extensions)
    result = {}
    for root, dirs, files in os.walk(watch_dir):
        if not recursive:
            dirs.clear()
        for name in files:
            if os.path.splitext(name)[1].lower() not in ext_set:
                continue
            filepath = os.path.join(root, name)
            abs_path = os.path.abspath(filepath)
            try:
                st = os.stat(abs_path)
                result[abs_path] = {"mtime": st.st_mtime, "size": st.st_size}
            except OSError:
                continue
    return result


def _send_file(server_url, client_id, filepath, event_type="created"):
    """Read and send a single file to the server."""
    try:
        with open(filepath, "rb") as fh:
            content = base64.b64encode(fh.read()).decode("utf-8")
    except OSError as exc:
        print(f"[sync] cannot read {filepath}: {exc}", file=sys.stderr)
        return False
    payload = {
        "event_type": event_type,
        "file_path": filepath,
        "client_id": client_id,
        "file_content": content,
    }
    try:
        resp = requests.post(f"{server_url}/api/watch-event", json=payload, timeout=10)
        if resp.status_code in (200, 201):
            return True
        print(f"[sync] {filepath} -> HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
    except requests.RequestException as exc:
        print(f"[sync] failed to send {filepath}: {exc}", file=sys.stderr)
    return False


def _sync_with_state(server_url, client_id, watch_dir, extensions, recursive, state):
    """Compare filesystem vs saved state, send only the diff."""
    current = _scan_directory(watch_dir, extensions, recursive)
    saved = state.files

    new_files = [p for p in current if p not in saved]
    deleted_files = [p for p in saved if p not in current]
    modified_files = [
        p for p in current
        if p in saved and (current[p]["mtime"] != saved[p]["mtime"] or current[p]["size"] != saved[p]["size"])
    ]

    count = 0
    for fp in new_files:
        if _send_file(server_url, client_id, fp, "created"):
            state.update(fp, current[fp]["mtime"], current[fp]["size"])
            count += 1
    for fp in modified_files:
        if _send_file(server_url, client_id, fp, "modified"):
            state.update(fp, current[fp]["mtime"], current[fp]["size"])
            count += 1
    for fp in deleted_files:
        payload = {
            "event_type": "deleted",
            "file_path": fp,
            "client_id": client_id,
        }
        try:
            resp = requests.post(f"{server_url}/api/watch-event", json=payload, timeout=10)
            if resp.status_code in (200, 201):
                state.remove(fp)
                count += 1
        except requests.RequestException as exc:
            print(f"[sync] failed to delete {fp}: {exc}", file=sys.stderr)

    state.save()
    return count, len(new_files), len(modified_files), len(deleted_files)


def _register_client(server_url, client_id, watched_dir):
    try:
        resp = requests.post(
            f"{server_url}/api/watch-clients",
            json={"client_id": client_id, "watched_dir": watched_dir},
            timeout=10,
        )
        if resp.status_code in (200, 201):
            print(f"[watch] registered client '{client_id}' on server")
        else:
            print(f"[watch] registration failed: HTTP {resp.status_code}", file=sys.stderr)
    except requests.RequestException as exc:
        print(f"[watch] failed to register client: {exc}", file=sys.stderr)


def main():
    default_server = os.environ.get("IR_SERVER_URL", "http://localhost:5000")

    parser = argparse.ArgumentParser(
        description="IR System file watcher client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s ./my_docs
  %(prog)s ./my_docs --server http://192.168.1.100:5000
  %(prog)s ./my_docs --recursive --ext .txt,.pdf
  %(prog)s ./my_docs --debounce 5.0 --no-register
""",
    )
    parser.add_argument("directory", help="directory to monitor for file changes")
    parser.add_argument(
        "-s", "--server",
        default=default_server,
        help=f"IR server URL (default: $IR_SERVER_URL or {default_server})",
    )
    parser.add_argument(
        "-c", "--client-id",
        default=os.uname().nodename if hasattr(os, "uname") else "watch-client",
        help="unique client identifier (default: hostname)",
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="watch subdirectories recursively",
    )
    parser.add_argument(
        "-e", "--ext",
        default=",".join(DEFAULT_EXTENSIONS),
        help=f"comma-separated file extensions to watch (default: {','.join(DEFAULT_EXTENSIONS)})",
    )
    parser.add_argument(
        "-d", "--debounce",
        type=float,
        default=2.0,
        help="ignore repeated events for the same file within N seconds (default: 2.0)",
    )
    parser.add_argument(
        "-f", "--state-file",
        default=None,
        help=f"path to state file (default: <dir>/{DEFAULT_STATE_FILE})",
    )
    parser.add_argument(
        "--no-register",
        action="store_true",
        help="do not register this client on the server at startup",
    )
    args = parser.parse_args()

    watch_dir = os.path.abspath(args.directory)
    if not os.path.isdir(watch_dir):
        parser.error(f"not a directory: {args.directory}")

    extensions = []
    for e in args.ext.split(","):
        e = e.strip()
        if not e:
            continue
        extensions.append(e.lower() if e.startswith(".") else "." + e.lower())

    server_url = args.server.rstrip("/")
    if not server_url.startswith("http"):
        server_url = "http://" + server_url

    state_path = args.state_file or os.path.join(watch_dir, DEFAULT_STATE_FILE)
    state = WatchState(state_path)

    if not args.no_register:
        _register_client(server_url, args.client_id, watch_dir)

    total, n_new, n_mod, n_del = _sync_with_state(
        server_url, args.client_id, watch_dir, extensions, args.recursive, state
    )
    if total:
        print(f"[sync] {total} file(s) synced: {n_new} new, {n_mod} modified, {n_del} deleted")
    else:
        print("[sync] directory is up to date")

    handler = WatchEventHandler(server_url, args.client_id, extensions, state, debounce=args.debounce)
    observer = Observer()
    observer.schedule(handler, watch_dir, recursive=args.recursive)
    observer.start()

    print(f"[watch] monitoring {watch_dir} (recursive={args.recursive})")
    print(f"[watch] extensions: {','.join(extensions)}")
    print(f"[watch] state file: {state_path}")
    print(f"[watch] server: {server_url}/api/watch-event")
    print("[watch] Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
