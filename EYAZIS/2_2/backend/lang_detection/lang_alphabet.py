"""
Alphabet-based language identification (Variant 7): EN vs FR.

Idea: French has signature diacritics (e e e a c oe ...) that never
occur in native English words. Score = share of French-specific letters
among all letters. Marker words (le/la/les/des/une/est/pour vs
the/and/of/to/in) break ties when no diacritics are present.

Decision rule (threshold tuned on the training corpus, stored in
alphabet.json):
  fr_score = W_DIA * diacritic_ratio + W_MARK * marker_ratio
  lang = fr if fr_score >= threshold else en

Stdlib only (no sklearn) — works in a bare interpreter.
"""
import json
import os
import re
import time
from typing import Dict, List, Tuple

from lang_detection.lang_text import FR_EXTRA, preprocess_for_lang
from lang_detection.lang_text import chunk_text
LANG_EN = "en"
LANG_FR = "fr"

PROFILES_DIR = os.path.join(os.path.dirname(__file__), "lang_profiles")
ALPHABET_PATH = os.path.join(PROFILES_DIR, "alphabet.json")

# French-specific letters (never native to English).
FR_DIACRITICS = set("àâäéèêëîïôöùûüçœæÿ")

# Frequent function words that separate the languages on plain ASCII text.
FR_MARKERS = {
    "le", "la", "les", "des", "une", "est", "pour", "dans", "avec", "plus",
    "tout", "cette", "sont", "être", "nous", "vous", "ils", "elles", "qui",
    "que", "pas", "sur", "par", "mais", "comme", "aux", "ces", "son", "sa",
}
EN_MARKERS = {
    "the", "and", "for", "with", "that", "this", "from", "have", "were",
    "been", "are", "was", "which", "their", "there", "what", "when",
    "where", "would", "could", "about", "into", "than", "them", "then",
}

W_DIA = 1.0   # weight of the diacritic ratio
W_MARK = 0.5  # weight of the marker-word ratio
DEFAULT_THRESHOLD = 0.01

_cached: dict = {}
_cached_mtime: float = 0.0


def default_params() -> dict:
    return {
        "method": "alphabet_diacritics_markers",
        "fr_diaccritics": sorted(FR_DIACRITICS),
        "fr_markers": sorted(FR_MARKERS),
        "en_markers": sorted(EN_MARKERS),
        "w_dia": W_DIA,
        "w_mark": W_MARK,
        "threshold": DEFAULT_THRESHOLD,
    }


def save_params(params: dict) -> str:
    global _cached, _cached_mtime
    os.makedirs(PROFILES_DIR, exist_ok=True)
    with open(ALPHABET_PATH, "w", encoding="utf-8") as fh:
        json.dump(params, fh, ensure_ascii=False, indent=2)
    _cached = {}
    _cached_mtime = 0.0
    return ALPHABET_PATH


def load_params() -> dict:
    global _cached, _cached_mtime
    if not os.path.exists(ALPHABET_PATH):
        return default_params()
    mtime = os.path.getmtime(ALPHABET_PATH)
    if not _cached or _cached_mtime != mtime:
        with open(ALPHABET_PATH, encoding="utf-8") as fh:
            _cached = json.load(fh)
        _cached_mtime = mtime
    return _cached


def is_trained() -> bool:
    return os.path.exists(ALPHABET_PATH)


def score_text(text: str, params: dict = None) -> dict:
    """Raw alphabet scores without applying the threshold."""
    params = params or load_params()
    cleaned = preprocess_for_lang(text)
    letters = [ch for ch in cleaned if ch.isalpha()]
    if not letters:
        raise ValueError("No classifiable text (empty after preprocessing)")
    dia = set(params.get("fr_diaccritics", sorted(FR_DIACRITICS)))
    dia_count = sum(1 for ch in letters if ch in dia)
    words = re.findall(r"[a-z" + re.escape(FR_EXTRA) + r"]+", cleaned)
    fr_mark = set(params.get("fr_markers", []))
    en_mark = set(params.get("en_markers", []))
    fr_hits = sum(1 for w in words if w in fr_mark)
    en_hits = sum(1 for w in words if w in en_mark)
    total_words = len(words) or 1
    dia_ratio = dia_count / len(letters)
    mark_ratio = (fr_hits - en_hits) / total_words
    fr_score = params.get("w_dia", W_DIA) * dia_ratio + params.get("w_mark", W_MARK) * mark_ratio
    return {
        "fr_ratio": round(dia_ratio, 5),
        "fr_marker_hits": fr_hits,
        "en_marker_hits": en_hits,
        "fr_score": round(fr_score, 5),
    }


def classify_text(text: str, params: dict = None) -> dict:
    """Classify raw text. Returns lang + scores + timing."""
    params = params or load_params()
    t0 = time.perf_counter()
    scores = score_text(text, params)
    threshold = params.get("threshold", DEFAULT_THRESHOLD)
    winner = LANG_FR if scores["fr_score"] >= threshold else LANG_EN
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return {
        "lang": winner,
        "threshold": threshold,
        "elapsed_ms": round(elapsed_ms, 2),
        **scores,
    }


def tune_threshold(en_texts: List[str], fr_texts: List[str]) -> dict:
    """Pick the threshold that best separates training scores.

    Uses chunk-level scores: threshold = midpoint between the worst FR
    score and the best EN score (falls back to DEFAULT_THRESHOLD if the
    classes overlap).
    """
    

    params = default_params()
    en_scores = [score_text(c, params)["fr_score"]
                 for t in en_texts for c in chunk_text(t)]
    fr_scores = [score_text(c, params)["fr_score"]
                 for t in fr_texts for c in chunk_text(t)]
    if en_scores and fr_scores:
        worst_fr = min(fr_scores)
        best_en = max(en_scores)
        threshold = (worst_fr + best_en) / 2 if worst_fr > best_en else DEFAULT_THRESHOLD
    else:
        threshold = DEFAULT_THRESHOLD
    params["threshold"] = round(threshold, 5)
    params["train_en_chunks"] = len(en_scores)
    params["train_fr_chunks"] = len(fr_scores)
    save_params(params)
    return params


def train(en_texts: List[str], fr_texts: List[str]) -> Dict:
    """Tune + save the alphabet threshold. Returns training metadata."""
    t0 = time.perf_counter()
    params = tune_threshold(en_texts, fr_texts)
    return {
        "method": "alphabet_diacritics_markers",
        "threshold": params["threshold"],
        "train_en_chunks": params["train_en_chunks"],
        "train_fr_chunks": params["train_fr_chunks"],
        "train_seconds": round(time.perf_counter() - t0, 2),
    }


def batch_accuracy(pairs: List[Tuple[str, str]]) -> Tuple[float, dict]:
    """Self-check on (true_lang, text) pairs. Returns (accuracy, confusion)."""
    from lang_detection.lang_text import batch_metrics

    pred = [classify_text(text)["lang"] for _, text in pairs]
    return batch_metrics([t for t, _ in pairs], pred)
