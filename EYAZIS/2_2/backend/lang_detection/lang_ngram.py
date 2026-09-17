"""
N-gram language identification (Variant 7): Cavnar & Trenkle out-of-place.

  - Profile: char n-grams (n=1..5) with space padding, counted over the
    training corpus, top-K (K=300) by frequency -> {ngram: rank}.
  - Document profile: same procedure on the input text.
  - Distance: sum of |rank_doc - rank_lang|; an n-gram missing from the
    language profile gets penalty MAX_PENALTY (= K).
  - Winner: language with the minimum distance.

Stdlib only (no sklearn) — works in a bare interpreter.
Preprocessing: lang_text.preprocess_for_lang (keeps FR diacritics).
"""
import json
import os
import time
from collections import Counter
from typing import Dict, List, Tuple

from lang_detection.lang_text import preprocess_for_lang, batch_metrics

LANG_EN = "en"
LANG_FR = "fr"

PROFILES_DIR = os.path.join(os.path.dirname(__file__), "lang_profiles")
NGRAM_EN_PATH = os.path.join(PROFILES_DIR, "ngram_en.json")
NGRAM_FR_PATH = os.path.join(PROFILES_DIR, "ngram_fr.json")

N_MIN = 1
N_MAX = 5
TOP_K = 300
MAX_PENALTY = TOP_K  # penalty for an n-gram absent from a language profile

_cached: Dict[str, dict] = {}
_cached_mtime: Dict[str, float] = {}


def extract_ngrams(text: str, n_min: int = N_MIN, n_max: int = N_MAX) -> Counter:
    """Char n-grams with single-space padding on both ends of the text."""
    counts: Counter = Counter()
    padded = f" {text} "
    for n in range(n_min, n_max + 1):
        if len(padded) < n:
            continue
        for i in range(len(padded) - n + 1):
            counts[padded[i:i + n]] += 1
    return counts


def build_profile(texts: List[str], top_k: int = TOP_K) -> List[str]:
    """Top-K n-grams (ordered) over a list of training texts."""
    total: Counter = Counter()
    for text in texts:
        total.update(extract_ngrams(preprocess_for_lang(text)))
    return [gram for gram, _ in total.most_common(top_k)]


def save_profile(lang: str, profile: List[str]) -> str:
    os.makedirs(PROFILES_DIR, exist_ok=True)
    path = NGRAM_EN_PATH if lang == LANG_EN else NGRAM_FR_PATH
    payload = {
        "lang": lang,
        "method": "cavnar_trenkle_out_of_place",
        "n_min": N_MIN,
        "n_max": N_MAX,
        "top_k": TOP_K,
        "max_penalty": MAX_PENALTY,
        "profile": profile,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    _cached.pop(lang, None)
    _cached_mtime.pop(lang, None)
    return path


def load_profile(lang: str) -> dict:
    path = NGRAM_EN_PATH if lang == LANG_EN else NGRAM_FR_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No N-gram profile at {path}. Train via POST /api/lang/train."
        )
    mtime = os.path.getmtime(path)
    if lang not in _cached or _cached_mtime.get(lang) != mtime:
        with open(path, encoding="utf-8") as fh:
            _cached[lang] = json.load(fh)
        _cached_mtime[lang] = mtime
    return _cached[lang]


def is_trained() -> bool:
    return os.path.exists(NGRAM_EN_PATH) and os.path.exists(NGRAM_FR_PATH)


def out_of_place_distance(doc_profile: List[str], lang_profile: List[str]) -> int:
    """Sum of rank differences; MAX_PENALTY for n-grams missing from lang."""
    rank = {gram: i for i, gram in enumerate(lang_profile)}
    dist = 0
    for i, gram in enumerate(doc_profile):
        if gram in rank:
            dist += abs(i - rank[gram])
        else:
            dist += MAX_PENALTY
    return dist


def classify_text(text: str, top_k: int = TOP_K) -> dict:
    """Classify raw text. Returns lang + both distances + timing."""
    t0 = time.perf_counter()
    cleaned = preprocess_for_lang(text)
    if not cleaned:
        raise ValueError("No classifiable text (empty after preprocessing)")
    doc_profile = [gram for gram, _ in extract_ngrams(cleaned).most_common(top_k)]
    dist_en = out_of_place_distance(doc_profile, load_profile(LANG_EN)["profile"])
    dist_fr = out_of_place_distance(doc_profile, load_profile(LANG_FR)["profile"])
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    winner = LANG_EN if dist_en <= dist_fr else LANG_FR
    margin = abs(dist_en - dist_fr)
    return {
        "lang": winner,
        "dist_en": dist_en,
        "dist_fr": dist_fr,
        "margin": margin,
        "elapsed_ms": round(elapsed_ms, 2),
    }


def train(en_texts: List[str], fr_texts: List[str]) -> dict:
    """Build + save both language profiles. Returns training metadata."""
    t0 = time.perf_counter()
    en_profile = build_profile(en_texts)
    fr_profile = build_profile(fr_texts)
    save_profile(LANG_EN, en_profile)
    save_profile(LANG_FR, fr_profile)
    return {
        "method": "cavnar_trenkle_out_of_place",
        "n_min": N_MIN,
        "n_max": N_MAX,
        "top_k": TOP_K,
        "max_penalty": MAX_PENALTY,
        "en_profile_size": len(en_profile),
        "fr_profile_size": len(fr_profile),
        "train_seconds": round(time.perf_counter() - t0, 2),
    }


def batch_accuracy(pairs: List[Tuple[str, str]]) -> Tuple[float, dict]:
    """Self-check on (true_lang, text) pairs. Returns (accuracy, confusion)."""
    pred = [classify_text(text)["lang"] for _, text in pairs]
    return batch_metrics([t for t, _ in pairs], pred)
