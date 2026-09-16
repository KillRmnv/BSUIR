"""
Orchestrator for the three Variant 7 methods: N-gram, alphabet, neural.

  - train_all(en_texts, fr_texts): trains every method, returns per-method
    metadata (neural part raises RuntimeError without sklearn).
  - classify_text_all / classify_html_all: run all trained methods,
    final lang = majority vote, agreed = all three agree.
  - classify_batch_all: batch + per-method accuracy/confusion/avg-ms.

Response shape is backward compatible with the neural-only API:
top-level lang/proba_en/proba_fr/elapsed_ms stay (neural values),
and a `methods` block plus `agreed` flag are added.
"""
import time
from typing import Dict, List, Tuple

from lang_detection import lang_alphabet
from lang_detection import lang_ngram
from lang_detection.lang_text import batch_metrics, extract_text_from_html_bytes

METHODS = ("ngram", "alphabet", "neural")


def train_all(en_texts: List[str], fr_texts: List[str]) -> dict:
    """Train all three methods. Neural needs sklearn; others are stdlib."""
    from lang_detection import lang_detect

    meta = {
        "ngram": lang_ngram.train(en_texts, fr_texts),
        "alphabet": lang_alphabet.train(en_texts, fr_texts),
        "neural": lang_detect.train(en_texts, fr_texts),
    }
    return meta


def status_all() -> dict:
    from lang_detection import lang_detect

    neural_trained = lang_detect.is_trained()
    return {
        "trained": neural_trained and lang_ngram.is_trained() and lang_alphabet.is_trained(),
        "methods": {
            "ngram": {"trained": lang_ngram.is_trained()},
            "alphabet": {"trained": lang_alphabet.is_trained()},
            "neural": {
                "trained": neural_trained,
                "metadata": lang_detect.get_metadata() if neural_trained else None,
            },
        },
    }


def _majority(votes: List[str]) -> Tuple[str, bool]:
    winner = max(set(votes), key=votes.count)
    return winner, len(set(votes)) == 1


def _try_method(fn, text: str):
    """Run one method; return None if it is unavailable (not trained)."""
    try:
        return fn(text)
    except (FileNotFoundError, RuntimeError):
        return None


def classify_text_all(text: str) -> dict:
    """Run all trained methods on raw text + majority vote.

    Methods that are not trained (e.g. neural without sklearn) are skipped:
    the vote goes over the available ones, missing entries are null.
    """
    from lang_detection import lang_detect

    t0 = time.perf_counter()
    ngram_res = lang_ngram.classify_text(text)
    alphabet_res = lang_alphabet.classify_text(text)
    neural_res = _try_method(lang_detect.classify_text, text)
    methods = {"ngram": ngram_res, "alphabet": alphabet_res, "neural": neural_res}
    votes = [r["lang"] for r in methods.values() if r is not None]
    if not votes:
        raise RuntimeError("No language method is trained")
    winner, agreed = _majority(votes)
    total_ms = (time.perf_counter() - t0) * 1000.0
    neural = neural_res or {}
    if neural and "metadata" not in neural:
        from lang_detection import lang_detect
        neural["metadata"] = lang_detect.get_metadata()
    return {
        "lang": winner,
        "agreed": agreed,
        "methods": methods,
        # neural values kept at top level when available (backward compatible)
        "proba_en": neural.get("proba_en"),
        "proba_fr": neural.get("proba_fr"),
        "elapsed_ms": round(total_ms, 2),
        "method": "vote_ngram_alphabet_neural",
    }


def classify_html_all(data: bytes, filename: str = "document.html") -> dict:
    text = extract_text_from_html_bytes(data)
    result = classify_text_all(text)
    result["title"] = filename.rsplit(".", 1)[0] if "." in filename else filename
    result["chars"] = len(text)
    return result


def classify_batch_all(items: List[Tuple[str, bytes]],
                       true_labels: Dict[str, str] = None) -> dict:
    """Classify many (filename, html_bytes) pairs with per-method summary."""
    true_labels = true_labels or {}
    documents: List[dict] = []
    for filename, data in items:
        try:
            res = classify_html_all(data, filename)
        except Exception as e:  # one bad file must not kill the batch
            documents.append({"title": filename, "error": str(e)})
            continue
        res["true_lang"] = true_labels.get(filename, "?")
        res["correct"] = res["true_lang"] in ("en", "fr") and res["lang"] == res["true_lang"]
        documents.append(res)

    ok = [d for d in documents if "methods" in d]
    summary: Dict = {}
    if ok:
        summary["avg_time_ms"] = round(sum(d["elapsed_ms"] for d in ok) / len(ok), 2)
    known = [d for d in ok if d["true_lang"] in ("en", "fr")]
    if known:
        acc, matrix = batch_metrics(
            [d["true_lang"] for d in known], [d["lang"] for d in known]
        )
        summary.update({
            "accuracy": round(acc, 4),
            "correct": sum(1 for d in known if d["correct"]),
            "total": len(known),
            "confusion": matrix,
        })
        per_method: Dict = {}
        for m in METHODS:
            scored = [(d["true_lang"], d["methods"][m]["lang"])
                      for d in known if d["methods"].get(m) is not None]
            if not scored:
                per_method[m] = {"trained": False}
                continue
            m_acc, m_matrix = batch_metrics([t for t, _ in scored],
                                            [p for _, p in scored])
            m_ms = [d["methods"][m]["elapsed_ms"] for d in known
                    if d["methods"].get(m) is not None]
            per_method[m] = {
                "trained": True,
                "accuracy": round(m_acc, 4),
                "confusion": m_matrix,
                "avg_time_ms": round(sum(m_ms) / len(m_ms), 2) if m_ms else 0,
            }
        summary["per_method"] = per_method
    return {"documents": documents, "total": len(documents), "summary": summary}
