import os
import glob
from data.database_manager import (
    init_db,
    get_all_document_texts,
    load_vocabulary,
    load_idf,
    save_vocabulary,
    save_idf,
    get_documents_without_summary,
    update_document_summary,
)
from search.document_processor import build_vocabulary, compute_idf
from search import document_processor as dp
from lang_detection.lang_methods import classify_text_all, status_all, train_all
from translator.seed_dictionary import seed as _seed_dictionary


def _classify_lang(text: str) -> str:
    try:
        result = classify_text_all(text)
        return result.get("lang", "en")
    except Exception:
        return "en"


def _backfill_summaries():
    docs = get_documents_without_summary()
    if not docs:
        return 0
    for doc in docs:
        summary = dp.generate_summary(doc["content"], lang=doc.get("lang", "en"))
        if summary:
            update_document_summary(doc["id"], summary)
    return len(docs)


def initialize_corpus(engine, base_dir: str) -> dict:
    init_db()
    try:
        _seed_dictionary()
    except Exception as e:
        print(f"Dictionary seed skipped: {e}")
    docs_dir = os.path.join(base_dir, "documents")
    txt_files = glob.glob(os.path.join(docs_dir, "*.txt"))
    if txt_files:
        texts = []
        langs = []
        for f in txt_files:
            with open(f, "r", encoding="utf-8") as fh:
                content = fh.read()
            texts.append(content)
            langs.append(_classify_lang(content))
        build_vocabulary(texts, langs=langs)
        compute_idf(texts, langs=langs)
        save_vocabulary(dp.VOCAB)
        save_idf(dp.IDF)
        for i, f in enumerate(txt_files):
            with open(f, "r", encoding="utf-8") as fh:
                content = fh.read()
            title = os.path.basename(f).rsplit(".", 1)[0]
            engine.index_documents([{"title": title, "content": content, "lang": langs[i]}])
    return {"message": "Database initialized", "documents_loaded": len(txt_files)}


def ensure_corpus(engine, base_dir: str):
    init_db()
    try:
        _seed_dictionary()
    except Exception as e:
        print(f"Dictionary seed skipped: {e}")
    all_docs = get_all_document_texts()
    if not all_docs:
        docs_dir = os.path.join(base_dir, "documents")
        txt_files = glob.glob(os.path.join(docs_dir, "*.txt"))
        if txt_files:
            texts = []
            langs = []
            for f in txt_files:
                with open(f, "r", encoding="utf-8") as fh:
                    content = fh.read()
                texts.append(content)
                langs.append(_classify_lang(content))
            build_vocabulary(texts, langs=langs)
            compute_idf(texts, langs=langs)
            save_vocabulary(dp.VOCAB)
            save_idf(dp.IDF)
            for i, f in enumerate(txt_files):
                with open(f, "r", encoding="utf-8") as fh:
                    content = fh.read()
                title = os.path.basename(f).rsplit(".", 1)[0]
                engine.index_documents([{"title": title, "content": content, "lang": langs[i]}])
    else:
        saved_vocab = load_vocabulary()
        saved_idf = load_idf()
        if saved_vocab:
            dp.VOCAB = saved_vocab
        if saved_idf:
            dp.IDF = saved_idf
        _backfill_summaries()


def ensure_lang_model(base_dir: str):
    try:
        if status_all()["trained"]:
            return
    except Exception:
        pass
    en_path = os.path.join(base_dir, "lang_detection", "training", "en.txt")
    fr_path = os.path.join(base_dir, "lang_detection", "training", "fr.txt")
    if not (os.path.exists(en_path) and os.path.exists(fr_path)):
        return
    try:
        with open(en_path, encoding="utf-8") as fh:
            en_text = fh.read()
        with open(fr_path, encoding="utf-8") as fh:
            fr_text = fh.read()
        train_all([en_text], [fr_text])
    except Exception:
        pass
