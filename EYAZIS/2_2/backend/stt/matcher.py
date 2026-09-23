"""Match recognized speech against editable command phrases (EN/FR).

Matching key is accent- and case-insensitive (Vosk often drops French
accents); the original phrase text is kept for reporting.
"""
import re
import unicodedata
from difflib import SequenceMatcher
from typing import List, Optional

FUZZY_THRESHOLD = 0.68
_PUNCT_RE = re.compile(r"[^\w\s']+", re.UNICODE)
_WS_RE = re.compile(r"\s+")


def strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def normalize(text: str) -> str:
    text = (text or "").strip().lower()
    text = strip_accents(text)
    text = _PUNCT_RE.sub(" ", text)
    text = _WS_RE.sub(" ", text).strip()
    return text


def _ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def _argument_after(phrase_norm: str, text_norm: str, takes_argument: bool) -> str:
    if not takes_argument:
        return ""
    if text_norm == phrase_norm:
        return ""
    if text_norm.startswith(phrase_norm):
        return text_norm[len(phrase_norm):].strip(" ,.!?;:")
    # phrase somewhere inside: keep words outside the matched span
    idx = text_norm.find(phrase_norm)
    if idx >= 0:
        before = text_norm[:idx].strip(" ,.!?;:")
        after = text_norm[idx + len(phrase_norm):].strip(" ,.!?;:")
        return (before + " " + after).strip() if before else after
    return text_norm if phrase_norm not in text_norm else ""


def match_command(text: str, operations: List[dict], lang: str) -> Optional[dict]:
    """Return best match {operation, argument, confidence, matched_phrase} or None."""
    text_norm = normalize(text)
    if not text_norm:
        return None

    best = None  # (score, phrase_len, payload)
    text_tokens = text_norm.split()

    for op in operations:
        phrases = (op.get("phrases") or {}).get(lang) or []
        # longest phrase first so "search for" wins over "search"
        for phrase in sorted(phrases, key=lambda p: len(normalize(p)), reverse=True):
            phrase_norm = normalize(phrase)
            if not phrase_norm:
                continue

            score = 0.0
            if text_norm == phrase_norm:
                score = 1.0
            elif text_norm.startswith(phrase_norm + " "):
                score = 0.95
            elif f" {phrase_norm} " in f" {text_norm} ":
                score = 0.88
            else:
                r = _ratio(text_norm, phrase_norm)
                # prefix-ish fuzzy: first token equality boosts score
                t0 = text_tokens[0] if text_tokens else ""
                p0 = phrase_norm.split(" ", 1)[0]
                if t0 and t0 == p0:
                    r = max(r, 0.8)
                if r >= FUZZY_THRESHOLD:
                    score = round(r * 0.92, 4)
                # token coverage: partial ASR still keeps content words
                p_tokens = phrase_norm.split()
                if p_tokens and len(p_tokens) >= 2:
                    present = sum(1 for t in p_tokens if t in text_tokens)
                    coverage = present / len(p_tokens)
                    if coverage >= 0.6:
                        score = max(score, round(0.70 + 0.25 * coverage, 4))

            if score <= 0:
                continue

            payload = {
                "operation": op["id"],
                "argument": _argument_after(phrase_norm, text_norm, bool(op.get("takes_argument"))),
                "confidence": round(score, 4),
                "matched_phrase": phrase,
                "takes_argument": bool(op.get("takes_argument")),
                "client_action": op.get("client_action"),
            }
            key = (score, len(phrase_norm))
            if best is None or key > (best[0], best[1]):
                best = (score, len(phrase_norm), payload)

    if best is None or best[0] < FUZZY_THRESHOLD:
        return None
    return best[2]
