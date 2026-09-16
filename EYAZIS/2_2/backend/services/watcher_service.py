import base64
from watcher.watch_handler import handle_watch_event
from data.database_manager import register_watch_client, get_watch_clients
from services.errors import ValidationError


def process_watch_event(data: dict, vector_dim: int) -> dict:
    event_type = data.get("event_type")
    file_path = data.get("file_path")
    if not event_type or not file_path:
        raise ValidationError("event_type and file_path are required")
    file_content = None
    b64 = data.get("file_content")
    if b64:
        try:
            file_content = base64.b64decode(b64)
        except Exception:
            raise ValidationError("invalid file_content base64")
    return handle_watch_event(
        event_type,
        file_path,
        data.get("client_id", ""),
        file_content,
        data.get("old_path"),
        vector_dim,
    )


def register_client(client_id: str, watched_dir: str = "") -> dict:
    if not client_id:
        raise ValidationError("client_id is required")
    register_watch_client(client_id, watched_dir)
    return {"message": "Client registered", "client_id": client_id}


def list_clients() -> dict:
    clients = get_watch_clients()
    return {"clients": clients, "total": len(clients)}
