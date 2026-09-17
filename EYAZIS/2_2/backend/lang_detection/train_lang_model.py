#!/usr/bin/env python3
"""
CLI for EN/FR language identification, all three Variant 7 methods
(N-gram + alphabet + neural LogReg).

  python train_lang_model.py train [--train-dir training]
  python train_lang_model.py classify <file.html|file.txt>
  python train_lang_model.py batch [--test-dir test_html]

`batch` reads manifest.csv for true labels and prints per-method
accuracy, confusion matrix and mean time per document (for the report).
Works without the Flask app / database. Neural training needs sklearn;
N-gram and alphabet methods are stdlib-only.
"""
import argparse
import csv
import glob
import os
import sys
import time

from lang_detection import lang_alphabet
from lang_detection import lang_ngram
from lang_detection.lang_methods import classify_html_all, classify_text_all, classify_batch_all

sys.path.insert(0, os.path.dirname(__file__))

BASE = os.path.dirname(__file__)
METHODS = ("ngram", "alphabet", "neural")
METHOD_TITLE = {
    "ngram": "N-gram (Cavnar & Trenkle)",
    "alphabet": "Alphabet (diacritics + markers)",
    "neural": "Neural (LogReg + char TF-IDF 1-5)",
}


def cmd_train(train_dir: str) -> int:
    en_path = os.path.join(train_dir, "en.txt")
    fr_path = os.path.join(train_dir, "fr.txt")
    for path in (en_path, fr_path):
        if not os.path.exists(path):
            print(f"Missing {path}. Run `python build_lang_corpus.py` first.")
            return 1
    with open(en_path, encoding="utf-8") as fh:
        en_text = fh.read()
    with open(fr_path, encoding="utf-8") as fh:
        fr_text = fh.read()
    meta = {
        "ngram": lang_ngram.train([en_text], [fr_text]),
        "alphabet": lang_alphabet.train([en_text], [fr_text]),
    }
    try:
        from lang_detection import lang_detect
        meta["neural"] = lang_detect.train([en_text], [fr_text])
    except RuntimeError as e:
        meta["neural"] = {"skipped": str(e)}
    for method in METHODS:
        print(f"[{method}]")
        for key, value in meta[method].items():
            print(f"  {key}: {value}")
    return 0


def _print_result(result: dict) -> None:
    methods = result.get("methods", {})
    print(f"  lang: {result['lang']} (agreed={result.get('agreed')})")
    if methods.get("ngram"):
        n = methods["ngram"]
        print(f"  ngram: {n['lang']} dist_en={n['dist_en']} dist_fr={n['dist_fr']} "
              f"margin={n['margin']} {n['elapsed_ms']} ms")
    if methods.get("alphabet"):
        a = methods["alphabet"]
        print(f"  alphabet: {a['lang']} fr_ratio={a['fr_ratio']} "
              f"markers fr/en={a['fr_marker_hits']}/{a['en_marker_hits']} "
              f"score={a['fr_score']} thr={a['threshold']} {a['elapsed_ms']} ms")
    if methods.get("neural"):
        m = methods["neural"]
        print(f"  neural: {m['lang']} P(en)={m['proba_en']} P(fr)={m['proba_fr']} "
              f"{m['elapsed_ms']} ms")
    else:
        print("  neural: not trained (needs scikit-learn)")


def cmd_classify(path: str) -> int:
    with open(path, "rb") as fh:
        data = fh.read()
    try:
        if path.lower().endswith((".html", ".htm")):
            result = classify_html_all(data, os.path.basename(path))
        else:
            result = classify_text_all(data.decode("utf-8", errors="ignore"))
    except (FileNotFoundError, RuntimeError, ValueError) as e:
        print(f"Cannot classify: {e}")
        return 1
    _print_result(result)
    return 0


def cmd_batch(test_dir: str) -> int:
    manifest_path = os.path.join(test_dir, "manifest.csv")
    true_labels = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                true_labels[row["filename"]] = row["true_lang"]
    files = sorted(glob.glob(os.path.join(test_dir, "*.html")))
    if not files:
        print(f"No .html files in {test_dir}. Run `python build_lang_corpus.py` first.")
        return 1

    items = []
    for path in files:
        with open(path, "rb") as fh:
            items.append((os.path.basename(path), fh.read()))
    try:
        batch = classify_batch_all(items, true_labels)
    except (FileNotFoundError, RuntimeError, ValueError) as e:
        print(f"Cannot classify: {e}")
        return 1

    for doc in batch["documents"]:
        if "methods" not in doc:
            print(f"[ERROR] {doc.get('title')}: {doc.get('error')}")
            continue
        mark = "OK" if doc.get("correct") else "MISS"
        votes = "/".join(doc["methods"][m]["lang"] for m in METHODS
                         if doc["methods"].get(m) is not None)
        print(f"[{mark}] {doc['title']}: true={doc['true_lang']} "
              f"vote={doc['lang']} [{votes}] {doc['elapsed_ms']} ms")

    summary = batch.get("summary", {})
    print(f"\nVOTE accuracy={summary.get('accuracy')} "
          f"correct={summary.get('correct')}/{summary.get('total')} "
          f"avg={summary.get('avg_time_ms')} ms")
    for method in METHODS:
        pm = (summary.get("per_method") or {}).get(method, {})
        if pm.get("trained"):
            print(f"{METHOD_TITLE[method]}: accuracy={pm['accuracy']} "
                  f"avg={pm['avg_time_ms']} ms confusion={pm['confusion']}")
        else:
            print(f"{METHOD_TITLE[method]}: not trained")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="EN/FR 3-method classifier CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    p_train = sub.add_parser("train")
    p_train.add_argument("--train-dir", default=os.path.join(BASE, "training"))
    p_cls = sub.add_parser("classify")
    p_cls.add_argument("path")
    p_batch = sub.add_parser("batch")
    p_batch.add_argument("--test-dir", default=os.path.join(BASE, "test_html"))
    args = parser.parse_args()
    t0 = time.perf_counter()
    if args.command == "train":
        code = cmd_train(args.train_dir)
    elif args.command == "classify":
        code = cmd_classify(args.path)
    else:
        code = cmd_batch(args.test_dir)
    print(f"({time.perf_counter() - t0:.2f} s total)")
    return code


if __name__ == "__main__":
    sys.exit(main())
