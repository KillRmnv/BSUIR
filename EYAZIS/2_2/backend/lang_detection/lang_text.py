"""
HTML body extraction + language-oriented preprocessing (Variant 7: EN/FR).

Deliberately independent from `document_processor.clean_text`, which strips
everything except a-z (that would destroy French diacritics: e, a, c, oe).

No third-party dependencies — stdlib only, so this module works both inside
the Docker image and in a bare local interpreter.
"""
import html as html_module
import random
import re
from typing import List, Tuple

# French-specific letters that must survive preprocessing.
FR_EXTRA = "àâäéèêëîïôöùûüçœæÿ"

# [a-z] + French diacritics. Lowercase everything first, so no A-Z needed.
LETTER_RE = re.compile(f"[a-z{FR_EXTRA}]")
WORD_CHAR_RE = re.compile(f"[a-z{FR_EXTRA}'’-]")


def decode_bytes(data: bytes) -> str:
    for enc in ("utf-8", "cp1251", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="ignore")


def extract_body_text(raw_html: str) -> str:
    """Extract visible text from <body>, dropping scripts/styles/markup."""
    text = raw_html
    # Drop script/style/noscript blocks entirely (with their content).
    text = re.sub(
        r"<(script|style|noscript)[^>]*>.*?</\1>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # Prefer <body> content; fall back to the whole document.
    m = re.search(r"<body[^>]*>(.*)</body\s*>", text, flags=re.IGNORECASE | re.DOTALL)
    if m:
        text = m.group(1)
    # Drop remaining tags, unescape entities, normalize whitespace.
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_module.unescape(text)
    text = re.sub(r"[ \t\r]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def extract_text_from_html_bytes(data: bytes) -> str:
    return extract_body_text(decode_bytes(data))


def preprocess_for_lang(text: str) -> str:
    """Lowercase, keep a-z + French diacritics, drop digits/punctuation.

    Returns a normalized single-line string suitable for char n-gram models.
    """
    text = text.lower()
    # Keep letters, apostrophes/hyphens inside words, and spaces; rest -> space.
    text = re.sub(f"[^a-z{FR_EXTRA}'’\\-\\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?…])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def chunk_text(text: str, target_chars: int = 2000) -> List[str]:
    """Split text into ~target_chars chunks on sentence boundaries.

    Gives the classifier many training samples instead of one giant string.
    """
    sentences = split_sentences(text)
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0
    for sent in sentences:
        current.append(sent)
        current_len += len(sent) + 1
        if current_len >= target_chars:
            chunks.append(" ".join(current))
            current = []
            current_len = 0
    if current:
        chunks.append(" ".join(current))
    return [c for c in chunks if len(c.strip()) > 50]


def expand_to_size(paragraphs: List[str], target_bytes: int, seed: int = 7) -> str:
    """Deterministically shuffle/repeat paragraphs until ~target_bytes reached.

    Offline stand-in for a large Wikipedia corpus: char n-gram statistics stay
    representative because the underlying sentences are real running text.
    The seed + method are recorded in corpus_meta.json for the report.
    """
    rng = random.Random(seed)
    out: List[str] = []
    total = 0
    pool = list(paragraphs)
    while total < target_bytes:
        rng.shuffle(pool)
        for p in pool:
            out.append(p)
            total += len(p.encode("utf-8")) + 1
            if total >= target_bytes:
                break
    return "\n\n".join(out) + "\n"


def batch_metrics(true: List[str], pred: List[str]) -> Tuple[float, dict]:
    """Accuracy + 2x2 confusion matrix for labels 'en' / 'fr'."""
    labels = ("en", "fr")
    matrix = {t: {p: 0 for p in labels} for t in labels}
    correct = 0
    for t, p in zip(true, pred):
        if t in matrix and p in matrix[t]:
            matrix[t][p] += 1
        if t == p:
            correct += 1
    accuracy = correct / len(true) if true else 0.0
    return accuracy, matrix
