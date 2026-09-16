"""
Neural language identification (Variant 7): EN vs FR.

Model: LogisticRegression on character TF-IDF (1-5 grams).
Storage: backend/lang_profiles/ml_model.pkl (files + in-memory cache).
"""
import os
import pickle
import time
from typing import Dict, List, Optional, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from lang_detection.lang_text import (
    chunk_text,
    extract_text_from_html_bytes,
    preprocess_for_lang,
)

LANG_EN = "en"
LANG_FR = "fr"

PROFILES_DIR = os.path.join(os.path.dirname(__file__), "lang_profiles")
MODEL_PATH = os.path.join(PROFILES_DIR, "ml_model.pkl")

VECTORIZER_PARAMS = {
    "analyzer": "char",
    "ngram_range": (1, 5),
    "max_features": 5000,
    "lowercase": True,
}
CLASSIFIER_PARAMS = {
    "max_iter": 1000,
    "random_state": 42,
}

_cached_model: Optional[dict] = None
_cached_mtime: Optional[float] = None


def train(
    en_texts: List[str],
    fr_texts: List[str],
    chunk_chars: int = 2000,
) -> dict:
    """Train LogReg on char TF-IDF. Returns metadata dict (also pickled)."""


    t0 = time.perf_counter()
    samples: List[str] = []
    labels: List[str] = []
    for text in en_texts:
        for chunk in chunk_text(text, chunk_chars):
            samples.append(preprocess_for_lang(chunk))
            labels.append(LANG_EN)
    for text in fr_texts:
        for chunk in chunk_text(text, chunk_chars):
            samples.append(preprocess_for_lang(chunk))
            labels.append(LANG_FR)
    if not samples or len(set(labels)) < 2:
        raise ValueError("Need non-empty training texts for BOTH en and fr")

    vectorizer = TfidfVectorizer(**VECTORIZER_PARAMS)
    X = vectorizer.fit_transform(samples)

    X_train, X_hold, y_train, y_hold = train_test_split(
        X, labels, test_size=0.2, random_state=42, stratify=labels
    )
    clf = LogisticRegression(**CLASSIFIER_PARAMS)
    clf.fit(X_train, y_train)

    train_acc = float(accuracy_score(y_train, clf.predict(X_train)))
    hold_acc = float(accuracy_score(y_hold, clf.predict(X_hold)))
    elapsed = time.perf_counter() - t0

    metadata = {
        "method": "logreg_char_tfidf_1_5",
        "vectorizer_params": {
            "analyzer": "char",
            "ngram_range": list(VECTORIZER_PARAMS["ngram_range"]),
            "max_features": VECTORIZER_PARAMS["max_features"],
        },
        "classifier_params": CLASSIFIER_PARAMS,
        "n_samples": len(samples),
        "n_en_chunks": sum(1 for l in labels if l == LANG_EN),
        "n_fr_chunks": sum(1 for l in labels if l == LANG_FR),
        "train_accuracy": round(train_acc, 4),
        "holdout_accuracy": round(hold_acc, 4),
        "train_seconds": round(elapsed, 2),
    }

    os.makedirs(PROFILES_DIR, exist_ok=True)
    with open(MODEL_PATH, "wb") as fh:
        pickle.dump(
            {"vectorizer": vectorizer, "clf": clf, "metadata": metadata},
            fh,
        )
    global _cached_model, _cached_mtime
    _cached_model = None  # force reload with fresh mtime
    _cached_mtime = None
    return metadata


def load_model() -> dict:
    """Load cached model; reload if the pickle changed on disk."""
    global _cached_model, _cached_mtime
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"No trained model at {MODEL_PATH}. "
            "Train it via POST /api/lang/train or `python train_lang_model.py`."
        )
    mtime = os.path.getmtime(MODEL_PATH)
    if _cached_model is None or _cached_mtime != mtime:
        with open(MODEL_PATH, "rb") as fh:
            _cached_model = pickle.load(fh)
        _cached_mtime = mtime
    return _cached_model


def is_trained() -> bool:
    return os.path.exists(MODEL_PATH)


def get_metadata() -> Optional[dict]:
    if not is_trained():
        return None
    try:
        return load_model().get("metadata")
    except Exception:
        return None


def classify_text(text: str) -> dict:
    """Classify raw text. Returns lang + probabilities + timing."""
    bundle = load_model()
    vectorizer = bundle["vectorizer"]
    clf = bundle["clf"]

    t0 = time.perf_counter()
    cleaned = preprocess_for_lang(text)
    if not cleaned:
        raise ValueError("No classifiable text (empty after preprocessing)")
    proba = clf.predict_proba(vectorizer.transform([cleaned]))[0]
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    classes = list(clf.classes_)
    prob_map = {str(c): float(p) for c, p in zip(classes, proba)}
    winner = str(classes[int(proba.argmax())])
    return {
        "lang": winner,
        "proba_en": round(prob_map.get(LANG_EN, 0.0), 4),
        "proba_fr": round(prob_map.get(LANG_FR, 0.0), 4),
        "elapsed_ms": round(elapsed_ms, 2),
    }


def classify_html(data: bytes, filename: str = "document.html") -> dict:
    """Extract <body> text from HTML bytes and classify it."""
    text = extract_text_from_html_bytes(data)
    result = classify_text(text)
    result["title"] = filename.rsplit(".", 1)[0] if "." in filename else filename
    result["method"] = "neural_logreg_char_tfidf_1_5"
    result["chars"] = len(text)
    return result


def classify_batch(items: List[Tuple[str, bytes]]) -> dict:
    """Classify many (filename, html_bytes) pairs. Errors are per-file."""
    per_doc: List[dict] = []
    for filename, data in items:
        try:
            per_doc.append(classify_html(data, filename))
        except Exception as e:  # one bad file must not kill the batch
            per_doc.append({"title": filename, "error": str(e)})
    return {"documents": per_doc, "total": len(per_doc)}
