#!/usr/bin/env python3
"""
Generate offline training + test data for Variant 7 (EN/FR, HTML).

  python build_lang_corpus.py [--train-kb 80] [--test-chars 2500]

Outputs (all inside backend/):
  training/en.txt, training/fr.txt   -- training corpora for lang profiles
  training/corpus_meta.json          -- method, seed, sizes, sources (for report)
  test_html/*.html                   -- 10 test docs (~A4 each, EN/FR mixed)
  test_html/manifest.csv             -- filename,true_lang,chars

Deterministic (seed=7). No internet needed: uses lang_seeds.py.
Seeds now include ~37 paragraphs per language covering science, history,
arts, and technology topics from Wikipedia and curated sources.
"""
import argparse
import csv
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))

from lang_detection.lang_seeds import EN_TEST, EN_TRAIN, FR_TEST, FR_TRAIN  # noqa: E402
from lang_detection.lang_text import expand_to_size  # noqa: E402

BASE = os.path.dirname(__file__)
TRAIN_DIR = os.path.join(BASE, "training")
TEST_DIR = os.path.join(BASE, "test_html")
SEED = 7

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>body {{ font-family: serif; }} .note {{ color: gray; }}</style>
</head>
<body>
<h1>{title}</h1>
{noise}
{paragraphs}
</body>
</html>
"""

NOISE_BLOCKS = [
    '<script>var counter = 0; function track() { counter++; }</script>',
    '<style>.hidden { display: none; }</style>',
    '<nav><a href="#">Home</a> | <a href="#">Archive</a></nav>',
    '',
    '',
]


def kb_of(text: str) -> float:
    return len(text.encode("utf-8")) / 1024.0


def build_training(train_kb: int) -> dict:
    os.makedirs(TRAIN_DIR, exist_ok=True)
    meta = {
        "method": "seeded_shuffle_expand",
        "seed": SEED,
        "source": "lang_seeds.py (37 EN + 37 FR paragraphs: curated + Wikipedia)",
        "languages": {},
    }
    for lang, paras in (("en", EN_TRAIN), ("fr", FR_TRAIN)):
        text = expand_to_size(paras, train_kb * 1024, seed=SEED)
        path = os.path.join(TRAIN_DIR, f"{lang}.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        meta["languages"][lang] = {
            "file": f"{lang}.txt",
            "kb": round(kb_of(text), 1),
            "base_paragraphs": len(paras),
        }
        print(f"training/{lang}.txt: {kb_of(text):.1f} Kb")
    with open(os.path.join(TRAIN_DIR, "corpus_meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    return meta


def build_test(test_chars: int) -> list:
    os.makedirs(TEST_DIR, exist_ok=True)
    rng = random.Random(SEED)
    manifest = []
    topics_en = ["jazz_history", "water_cycle", "printing_press", "vaccination", "eiffel_tower"]
    topics_fr = ["histoire_du_jazz", "cycle_de_l_eau", "presse_imprimerie", "vaccination", "tour_eiffel"]
    for lang, paras, topics in (("en", EN_TEST, topics_en), ("fr", FR_TEST, topics_fr)):
        for para, topic in zip(paras, topics):
            text = expand_to_size([para], test_chars, seed=SEED + len(manifest))
            html_paras = "\n".join(f"<p>{p}</p>" for p in text.split("\n\n") if p.strip())
            noise = rng.choice(NOISE_BLOCKS)
            title = topic.replace("_", " ").title()
            html = HTML_TEMPLATE.format(lang=lang, title=title, noise=noise, paragraphs=html_paras)
            fname = f"{lang}_{topic}.html"
            with open(os.path.join(TEST_DIR, fname), "w", encoding="utf-8") as fh:
                fh.write(html)
            manifest.append({"filename": fname, "true_lang": lang, "chars": len(text)})
            print(f"test_html/{fname}: {len(text)} chars")
    with open(os.path.join(TEST_DIR, "manifest.csv"), "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["filename", "true_lang", "chars"])
        writer.writeheader()
        writer.writerows(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build EN/FR corpora + HTML tests (offline)")
    parser.add_argument("--train-kb", type=int, default=200)
    parser.add_argument("--test-chars", type=int, default=2500)
    args = parser.parse_args()
    build_training(args.train_kb)
    build_test(args.test_chars)
    print("Done.")


if __name__ == "__main__":
    main()
