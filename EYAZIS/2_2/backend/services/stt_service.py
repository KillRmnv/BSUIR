"""STT service: validate audio, recognize with Vosk, match commands, dispatch."""
import re
import time
import urllib.parse
from typing import Optional

from flask import current_app

from lang_detection.lang_methods import classify_text_all
from services import search_service, summarization_service, translation_service
from services.errors import ValidationError, ServiceError, NotFoundError
from stt import commands as command_registry
from stt import engines, matcher

MAX_WAV_BYTES = 8 * 1024 * 1024
_DOC_ID_RE = re.compile(r"(?:doc(?:ument)?|n°|no\.?)?\s*#?\s*(\d+)\b", re.IGNORECASE)


def status() -> dict:
    s = engines.status()
    s["commands"] = {
        "path": command_registry.COMMANDS_PATH,
        "operations": len(command_registry.get_operations()),
    }
    return s


def list_commands() -> dict:
    ops = command_registry.get_operations()
    return {
        "operations": ops,
        "defaults": command_registry.default_commands()["operations"],
    }


def update_commands(payload: dict) -> dict:
    data = command_registry.save_commands(payload)
    return {"operations": data["operations"], "saved": True}


def reset_commands() -> dict:
    data = command_registry.reset_commands()
    return {"operations": data["operations"], "reset": True}


def _notify(lang: str, en: str, fr: str) -> dict:
    return {"en": en, "fr": fr}


def _dispatch(match: dict, argument: str, lang: str,
              doc_id: Optional[str], engine) -> dict:
    op_id = match["operation"]

    if op_id == "search":
        if not argument:
            return {
                "result": {"need_query": True},
                "client_action": None,
                "notify": _notify(
                    lang,
                    "Add a query after the command, e.g. 'search for hamlet'.",
                    "Ajoutez une requête après la commande, ex. « rechercher hamlet ».",
                ),
            }
        if engine is None:
            raise ServiceError("search engine is not available")
        result = search_service.search_documents(engine, argument, top_k=5)
        titles = [r.get("title", "") for r in (result.get("results") or [])[:3]]
        total = result.get("total_found", len(result.get("results") or []))
        summary = ", ".join(t for t in titles if t) or "no results"
        q_enc = urllib.parse.quote(argument, safe="")
        return {
            "result": {
                "query": argument,
                "total_found": total,
                "top": titles,
                "query_lang": result.get("query_lang"),
            },
            "client_action": f"navigate:index.html?q={q_enc}",
            "notify": _notify(
                lang,
                f"Search for '{argument}': {total} results. Top: {summary}.",
                f"Recherche de « {argument} » : {total} résultats. Top : {summary}.",
            ),
        }

    if op_id == "summarize":
        resolved_doc_id = doc_id
        if argument:
            m = _DOC_ID_RE.search(argument)
            if m:
                resolved_doc_id = m.group(1)
        if not resolved_doc_id:
            return {
                "result": {"need_doc": True, "hint": "say e.g. 'summarize document 5'"},
                "client_action": None,
                "notify": _notify(
                    lang,
                    "Say a document id, e.g. 'summarize document 5'.",
                    "Dites l'identifiant du document, ex. « résumer le document 5 ».",
                ),
            }
        result = summarization_service.summarize_document(doc_id=int(resolved_doc_id))
        sent = result.get("summary") or result.get("sentences") or ""
        if isinstance(sent, list):
            sent = " ".join(str(s) for s in sent)
        preview = sent[:160]
        return {
            "result": result,
            "client_action": f"navigate:summarize.html?doc={resolved_doc_id}",
            "notify": _notify(
                lang,
                f"Summary of '{result.get('title', resolved_doc_id)}' is ready: {preview}...",
                f"Résumé de « {result.get('title', resolved_doc_id)} » prêt : {preview}...",
            ),
        }

    if op_id == "translate":
        if not argument:
            return {
                "result": {"need_text": True},
                "client_action": None,
                "notify": _notify(
                    lang,
                    "Add text after the command, e.g. 'translate hello world'.",
                    "Ajoutez du texte après la commande, ex. « traduire bonjour ».",
                ),
            }
        result = translation_service.translate(argument)
        translated = result.get("translation") or result.get("translated") or str(result)
        t_enc = urllib.parse.quote(argument, safe="")
        return {
            "result": result,
            "client_action": f"navigate:translate.html?text={t_enc}",
            "notify": _notify(
                lang,
                f"Translation: {translated}",
                f"Traduction : {translated}",
            ),
        }

    if op_id == "read_aloud":
        text_to_speak = argument or "Hello. This is the reading mode."
        return {
            "result": {"speak": text_to_speak},
            "client_action": None,
            "speak": text_to_speak,
            "notify": _notify(
                lang,
                f"Reading aloud: {text_to_speak[:120]}",
                f"Lecture à voix haute : {text_to_speak[:120]}",
            ),
        }

    if op_id == "detect_language":
        if not argument:
            return {
                "result": {"need_text": True},
                "client_action": None,
                "notify": _notify(
                    lang,
                    "Add a sentence after the command, e.g. 'detect language the sky is blue'.",
                    "Ajoutez une phrase après la commande, ex. « détecter la langue le ciel est bleu ».",
                ),
            }
        detected = classify_text_all(argument)
        dlang = detected.get("lang", "?")
        return {
            "result": {
                "lang": dlang,
                "agreed": detected.get("agreed"),
                "elapsed_ms": detected.get("elapsed_ms"),
            },
            "client_action": None,
            "notify": _notify(
                lang,
                f"Detected language: {dlang.upper()} (methods agreed: {detected.get('agreed')}).",
                f"Langue détectée : {dlang.upper()} (méthodes concordantes : {detected.get('agreed')}).",
            ),
        }

    if op_id == "list_commands":
        ops = command_registry.get_operations()
        ids = [o["id"] for o in ops]
        return {
            "result": {"operations": ops},
            "client_action": "navigate:stt.html?panel=commands",
            "notify": _notify(
                lang,
                f"{len(ids)} commands available: {', '.join(ids)}.",
                f"{len(ids)} commandes disponibles : {', '.join(ids)}.",
            ),
        }

    # pure client-side operations (open_*, help)
    action = match.get("client_action") or ""
    page = action.split(":", 1)[1] if ":" in action else "index.html"
    return {
        "result": {},
        "client_action": action or None,
        "notify": _notify(
            lang,
            f"Opening {page}.",
            f"Ouverture de {page}.",
        ),
    }


def recognize(wav_bytes: bytes, lang: str = "en",
              doc_id: Optional[str] = None, engine=None) -> dict:
    lang = (lang or "").strip().lower()
    if lang not in ("en", "fr"):
        raise ValidationError("lang must be 'en' or 'fr'")
    if not wav_bytes:
        raise ValidationError("audio file is required")
    if len(wav_bytes) > MAX_WAV_BYTES:
        raise ValidationError(f"audio file too large (max {MAX_WAV_BYTES} bytes)")

    ops = command_registry.get_operations()
    started = time.perf_counter()

    # dual-pass: free text (for arguments) + constrained vocab (for matching)
    pcm = engines.wav_to_pcm_safe(wav_bytes)
    text_free = engines.recognize_pcm(lang, pcm)
    vocab = command_registry.vocab_words(ops, lang)
    text_cmd = engines.recognize_pcm(lang, pcm, words=vocab) if vocab else text_free
    recognized_ms = round((time.perf_counter() - started) * 1000.0, 1)

    match_free = matcher.match_command(text_free, ops, lang) if text_free else None
    match_cmd = matcher.match_command(text_cmd, ops, lang) if text_cmd else None
    if match_free and match_cmd:
        match = match_free if match_free["confidence"] >= match_cmd["confidence"] else match_cmd
        # argument prefers the free (open-vocab) transcript
        if match is match_cmd and match_free["operation"] == match_cmd["operation"]:
            match = dict(match_cmd, argument=match_free.get("argument") or match_cmd.get("argument"))
    else:
        match = match_free or match_cmd

    # representative text: free transcript if it is non-empty, else constrained
    text = text_free or text_cmd

    base = {
        "text": text,
        "text_free": text_free,
        "text_cmd": text_cmd,
        "lang": lang,
        "recognized_ms": recognized_ms,
        "matched": match is not None,
    }

    if not match:
        base.update({
            "operation": None,
            "argument": None,
            "confidence": 0.0,
            "matched_phrase": None,
            "notify": _notify(
                lang,
                "Command not recognized. Say 'list commands' to see the options.",
                "Commande non reconnue. Dites « lister les commandes ».",
            ),
        })
        return base

    argument = match.get("argument") or ""
    dispatched = _dispatch(match, argument, lang, doc_id, engine)
    base.update({
        "operation": match["operation"],
        "argument": argument or None,
        "confidence": match["confidence"],
        "matched_phrase": match["matched_phrase"],
        "result": dispatched.get("result"),
        "client_action": dispatched.get("client_action"),
        "notify": dispatched.get("notify"),
    })
    if "speak" in dispatched:
        base["speak"] = dispatched["speak"]
    base["elapsed_ms"] = round((time.perf_counter() - started) * 1000.0, 1)
    return base
