"""Text normalization before synthesis.

The subject domain is literary essays (EN/FR): typographic quotes, dashes,
ellipsis, markdown artifacts and line breaks must be converted into
TTS-friendly punctuation so both engines read with natural pauses.
"""
import re

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_MD_DECOR_RE = re.compile(r"^[#>\-\*\+\t ]+", re.MULTILINE)
_WS_RE = re.compile(r"[ \t]+")
_LINE_RE = re.compile(r"\s*\n\s*")
_LONG_COMMA_RE = re.compile(r"[,;:]{2,}")
_LONG_DOT_RE = re.compile(r"\.{4,}")


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = _HTML_TAG_RE.sub(" ", text)
    text = _MD_DECOR_RE.sub("", text)
    # dashes -> short pause
    text = text.replace("\u2014", ", ").replace("\u2013", ", ").replace(" -- ", ", ")
    # ellipsis
    text = text.replace("\u2026", "...")
    # typographic quotes -> plain quotes
    text = re.sub(r"[\u00ab\u00bb]", '"', text)
    text = re.sub(r"[\u201c\u201d\u201e]", '"', text)
    text = re.sub(r"[\u2018\u2019]", "'", text)
    # strip common markdown emphasis left-overs inside lines
    text = re.sub(r"(\*\*|__|\*|_)([^*_]+)(\1)", r"\2", text)
    # collapse whitespace / line breaks
    text = _WS_RE.sub(" ", text)
    text = _LINE_RE.sub(" ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = _LONG_COMMA_RE.sub(",", text)
    text = _LONG_DOT_RE.sub("...", text)
    return text.strip()
