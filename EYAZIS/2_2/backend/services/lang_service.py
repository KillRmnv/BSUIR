import os
import csv as csv_module
import glob
from services.errors import ValidationError, ServiceError
from lang_detection.lang_methods import status_all, train_all, classify_html_all, classify_text_all, classify_batch_all


def status() -> dict:
    status = status_all()
    neural = status["methods"]["neural"]
    status["metadata"] = neural.get("metadata")
    return status


def train(base_dir: str) -> dict:
    en_path = os.path.join(base_dir, "lang_detection", "training", "en.txt")
    fr_path = os.path.join(base_dir, "lang_detection", "training", "fr.txt")
    if not os.path.exists(en_path) or not os.path.exists(fr_path):
        raise ValidationError("Training corpora not found. Run `python build_lang_corpus.py` first.")
    with open(en_path, encoding="utf-8") as fh:
        en_text = fh.read()
    with open(fr_path, encoding="utf-8") as fh:
        fr_text = fh.read()
    metadata = train_all([en_text], [fr_text])
    return {"message": "Language models trained (ngram + alphabet + neural)", "metadata": metadata}


def classify_file(file_storage) -> dict:
    return classify_html_all(file_storage.read(), file_storage.filename)


def classify_text(text: str) -> dict:
    return classify_text_all(text)


def classify_batch(base_dir: str) -> dict:
    test_dir = os.path.join(base_dir, "lang_detection", "test_html")
    manifest_path = os.path.join(test_dir, "manifest.csv")
    true_labels = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as fh:
            for row in csv_module.DictReader(fh):
                true_labels[row["filename"]] = row["true_lang"]
    files = sorted(glob.glob(os.path.join(test_dir, "*.html")))
    if not files:
        raise ValidationError("No test HTML files. Run `python build_lang_corpus.py` first.")
    items = []
    for path in files:
        with open(path, "rb") as fh:
            items.append((os.path.basename(path), fh.read()))
    return classify_batch_all(items, true_labels)
