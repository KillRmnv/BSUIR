"""Editable voice-command registry: fixed operations + user-defined phrases (EN/FR).

Phrases are stored in backend/data/stt_commands.json; operations and their
behaviour are fixed in code — the user may only edit the trigger phrases.
"""
import copy
import json
import os
import threading
from typing import List, Optional

from services.errors import ValidationError

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
COMMANDS_PATH = os.environ.get(
    "STT_COMMANDS_PATH",
    os.path.join(DATA_DIR, "stt_commands.json"),
)

# Fixed operations (variant 8): id / behaviour never change, only phrases do.
DEFAULT_OPERATIONS = [
    {
        "id": "search",
        "description": "Поиск документов / Search documents",
        "takes_argument": True,
        "client_action": None,
        "phrases": {
            "en": ["search for", "look up", "find documents about", "search"],
            "fr": ["rechercher", "chercher", "trouver des documents sur", "recherche"],
        },
    },
    {
        "id": "summarize",
        "description": "Реферирование документа / Summarize document",
        "takes_argument": True,
        "client_action": None,
        "phrases": {
            "en": ["summarize the document", "make a summary", "summarize", "sum up"],
            "fr": ["résumer le document", "faire un résumé", "résumer", "resume"],
        },
    },
    {
        "id": "translate",
        "description": "Перевод текста / Translate text",
        "takes_argument": True,
        "client_action": None,
        "phrases": {
            "en": ["translate", "translate this", "give a translation"],
            "fr": ["traduire", "traduire ce texte", "donner une traduction"],
        },
    },
    {
        "id": "read_aloud",
        "description": "Озвучить текст / Read text aloud (TTS)",
        "takes_argument": True,
        "client_action": None,
        "phrases": {
            "en": ["read aloud", "read the text", "speak this", "read"],
            "fr": ["lire à voix haute", "lire le texte", "lire", "dicte"],
        },
    },
    {
        "id": "detect_language",
        "description": "Определить язык / Detect language",
        "takes_argument": True,
        "client_action": None,
        "phrases": {
            "en": ["detect language", "what language is this", "identify the language"],
            "fr": ["détecter la langue", "quelle est cette langue", "identifier la langue"],
        },
    },
    {
        "id": "list_commands",
        "description": "Список команд / List available commands",
        "takes_argument": False,
        "client_action": None,
        "phrases": {
            "en": ["list commands", "what can you do", "show commands"],
            "fr": ["lister les commandes", "que peux-tu faire", "montrer les commandes"],
        },
    },
    {
        "id": "open_search",
        "description": "Открыть поиск / Open search page",
        "takes_argument": False,
        "client_action": "navigate:index.html",
        "phrases": {
            "en": ["open search", "go to search"],
            "fr": ["ouvrir la recherche", "aller à la recherche"],
        },
    },
    {
        "id": "open_documents",
        "description": "Открыть документы / Open documents page",
        "takes_argument": False,
        "client_action": "navigate:documents.html",
        "phrases": {
            "en": ["open documents", "show documents", "go to documents"],
            "fr": ["ouvrir les documents", "montrer les documents"],
        },
    },
    {
        "id": "open_summarize",
        "description": "Открыть реферирование / Open summarizer",
        "takes_argument": False,
        "client_action": "navigate:summarize.html",
        "phrases": {
            "en": ["open summarize", "go to summarizer", "open the summarizer"],
            "fr": ["ouvrir le résumé", "aller au résumé", "ouvrir le résumer"],
        },
    },
    {
        "id": "open_translate",
        "description": "Открыть переводчик / Open translator",
        "takes_argument": False,
        "client_action": "navigate:translate.html",
        "phrases": {
            "en": ["open translator", "go to translator", "open the translator"],
            "fr": ["ouvrir le traducteur", "aller au traducteur"],
        },
    },
    {
        "id": "open_classify",
        "description": "Открыть классификатор / Open language classifier",
        "takes_argument": False,
        "client_action": "navigate:classify.html",
        "phrases": {
            "en": ["open classifier", "open classification", "go to classifier"],
            "fr": ["ouvrir le classifieur", "ouvrir la classification", "aller au classifieur"],
        },
    },
    {
        "id": "open_upload",
        "description": "Открыть загрузку / Open upload page",
        "takes_argument": False,
        "client_action": "navigate:upload.html",
        "phrases": {
            "en": ["open upload", "go to upload", "upload a document"],
            "fr": ["ouvrir le téléversement", "aller au téléversement", "téléverser un document"],
        },
    },
    {
        "id": "open_metrics",
        "description": "Открыть метрики / Open metrics page",
        "takes_argument": False,
        "client_action": "navigate:metrics.html",
        "phrases": {
            "en": ["open metrics", "show metrics", "go to metrics", "open statistics"],
            "fr": ["ouvrir les métriques", "montrer les métriques", "ouvrir les statistiques"],
        },
    },
    {
        "id": "open_tts",
        "description": "Открыть озвучку / Open text-to-speech page",
        "takes_argument": False,
        "client_action": "navigate:tts.html",
        "phrases": {
            "en": ["open text to speech", "open speech synthesis", "open tts", "go to tts"],
            "fr": ["ouvrir la synthèse vocale", "ouvrir le tts", "aller au tts"],
        },
    },
    {
        "id": "open_stt",
        "description": "Открыть распознавание / Open speech recognition page",
        "takes_argument": False,
        "client_action": "navigate:stt.html",
        "phrases": {
            "en": ["open speech recognition", "open voice commands", "open stt", "go to voice"],
            "fr": ["ouvrir la reconnaissance vocale", "ouvrir les commandes vocales", "aller à la voix"],
        },
    },
    {
        "id": "help",
        "description": "Справка / Open help",
        "takes_argument": False,
        "client_action": "navigate:help.html",
        "phrases": {
            "en": ["open help", "show help", "help"],
            "fr": ["ouvrir l'aide", "montrer l'aide", "aide"],
        },
    },
]

_file_lock = threading.RLock()  # re-entrant: load_commands seeds via save_commands
_cache = {"path": None, "mtime": 0.0, "data": None}


def default_commands() -> dict:
    return {"version": 1, "operations": copy.deepcopy(DEFAULT_OPERATIONS)}


def _read_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict) or "operations" not in data:
        raise ValidationError("invalid stt_commands.json format")
    return data


def _sync_with_defaults(data: dict) -> tuple:
    """Merge DEFAULT_OPERATIONS into a loaded file (new open_* tabs, fixed fields).

    Phrases from the file are preserved; ids/description/behaviour always match
    DEFAULT_OPERATIONS. Returns (synced_data, changed).
    """
    incoming = data.get("operations") or []
    by_id = {}
    for op in incoming:
        if isinstance(op, dict) and op.get("id"):
            by_id[op["id"]] = op
    merged = []
    changed = len(incoming) != len(DEFAULT_OPERATIONS)
    for base in DEFAULT_OPERATIONS:
        cur = by_id.get(base["id"])
        if cur is None:
            merged.append(copy.deepcopy(base))
            changed = True
            continue
        item = copy.deepcopy(cur)
        for key in ("description", "takes_argument", "client_action"):
            if item.get(key) != base[key]:
                item[key] = base[key]
                changed = True
        phrases = item.get("phrases")
        if not isinstance(phrases, dict):
            item["phrases"] = copy.deepcopy(base["phrases"])
            changed = True
        else:
            for lang in ("en", "fr"):
                if not phrases.get(lang):
                    phrases[lang] = list(base["phrases"][lang])
                    changed = True
        merged.append(item)
    out = {"version": data.get("version", 1), "operations": merged}
    return out, changed


def load_commands() -> dict:
    """Load commands JSON with mtime cache; seed defaults if file missing."""
    path = COMMANDS_PATH
    with _file_lock:
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            mtime = 0.0
        if _cache["data"] is not None and _cache["path"] == path and _cache["mtime"] == mtime:
            return _cache["data"]
        if mtime == 0.0:
            data = default_commands()
            save_commands(data, force=True)
        else:
            try:
                data, changed = _sync_with_defaults(_read_file(path))
                if changed:
                    save_commands(data, force=True)
                    return _cache["data"]
            except (OSError, json.JSONDecodeError, ValidationError):
                data = default_commands()
        _cache.update(path=path, mtime=mtime, data=data)
        return data


def save_commands(data: dict, force: bool = False) -> dict:
    """Persist operations+phrases. Operation ids/behaviour must stay fixed."""
    if not isinstance(data, dict):
        raise ValidationError("commands payload must be an object")
    incoming = data.get("operations")
    if not isinstance(incoming, list) or not incoming:
        raise ValidationError("operations must be a non-empty list")

    defaults = {op["id"]: op for op in DEFAULT_OPERATIONS}
    merged = []
    seen = set()
    for item in incoming:
        if not isinstance(item, dict):
            raise ValidationError("operation entry must be an object")
        op_id = str(item.get("id", "")).strip()
        if op_id not in defaults:
            raise ValidationError(f"unknown operation: {op_id or '(empty)'}")
        if op_id in seen:
            raise ValidationError(f"duplicate operation: {op_id}")
        seen.add(op_id)
        base = defaults[op_id]
        phrases = item.get("phrases", base["phrases"])
        if not isinstance(phrases, dict):
            raise ValidationError(f"phrases for '{op_id}' must be an object")
        clean = {}
        for lang in ("en", "fr"):
            raw = phrases.get(lang, [])
            if not isinstance(raw, list):
                raise ValidationError(f"phrases.{lang} for '{op_id}' must be a list")
            items = []
            for p in raw:
                text = str(p).strip()
                if not text:
                    continue
                if len(text) > 80:
                    raise ValidationError(f"phrase too long (max 80 chars): {text[:40]}...")
                if text.lower() not in [t.lower() for t in items]:
                    items.append(text)
            if not items:
                raise ValidationError(f"operation '{op_id}' needs at least one phrase for {lang}")
            clean[lang] = items
        merged.append({
            "id": op_id,
            "description": base["description"],
            "takes_argument": bool(base["takes_argument"]),
            "client_action": base["client_action"],
            "phrases": clean,
        })

    if len(merged) != len(DEFAULT_OPERATIONS) and not force:
        # allow partial payload only when saving full set from UI
        missing = set(defaults) - seen
        if missing:
            raise ValidationError(f"missing operations: {', '.join(sorted(missing))}")

    result = {"version": 1, "operations": merged}
    path = COMMANDS_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with _file_lock:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
        _cache.update(path=path, mtime=os.path.getmtime(path), data=result)
    return result


def reset_commands() -> dict:
    data = default_commands()
    return save_commands(data, force=True)


def get_operations() -> List[dict]:
    return load_commands()["operations"]


def get_operation(op_id: str) -> Optional[dict]:
    for op in get_operations():
        if op["id"] == op_id:
            return op
    return None


def vocab_words(operations: List[dict], lang: str) -> List[str]:
    """All phrase tokens for the language — used to constrain Vosk decoding."""
    from stt.matcher import normalize
    words = set()
    for op in operations:
        for phrase in (op.get("phrases") or {}).get(lang) or []:
            words.update(normalize(phrase).split())
    return sorted(words)
