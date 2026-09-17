"""
Server-side processing of file-watcher events pushed by watch_client.py.

Flow for created/modified:
    base64 content -> extract text -> classify lang -> upload text to S3 -> rebuild vocab/IDF -> summary -> upsert by file_path
Flow for deleted:
    remove document by file_path -> delete from S3 -> rebuild vocab/IDF
"""
import os
import uuid
from typing import Dict, Optional

from flask import current_app
from doc_loader.document_loader import extract_text_from_bytes
from search.document_processor import (
    build_vocabulary,
    compute_idf,
    generate_summary,
    vectorize_text_with_dim,
    expand_vocabulary,
)
from search import document_processor as dp
from data.database_manager import (
    get_all_document_texts_with_lang,
    upsert_document,
    delete_document_by_path,
    save_vocabulary,
    save_idf,
    log_watch_event,
    load_vocabulary,
    load_idf,
    get_all_document_ids_and_contents,
    update_document_embedding,
)
from storage import s3_client
from lang_detection.lang_methods import classify_text_all


def _classify_lang(text: str) -> str:
    """Classify text language as 'en' or 'fr'. Falls back to 'en' on error."""
    try:
        result = classify_text_all(text)
        return result.get("lang", "en")
    except Exception:
        return "en"


def _rebuild_vocab_idf():
    doc_langs = get_all_document_texts_with_lang()
    if doc_langs:
        texts = [d[0] for d in doc_langs]
        langs = [d[1] for d in doc_langs]
        build_vocabulary(texts, langs=langs)
        compute_idf(texts, langs=langs)
        save_vocabulary(dp.VOCAB)
        save_idf(dp.IDF)
        _reembed_all()


def _reembed_all():
    """Re-embed all documents with the current VOCAB/IDF."""
    engine = current_app.config["ENGINE"]
    all_docs = get_all_document_ids_and_contents()
    for doc in all_docs:
        emb = vectorize_text_with_dim(doc["content"], engine.vector_dim, doc.get("lang", "en"))
        update_document_embedding(doc["id"], emb)


def handle_watch_event(
    event_type: str,
    file_path: str,
    client_id: str,
    file_content: Optional[bytes] = None,
    old_path: Optional[str] = None,
    vector_dim: int = 5000,
) -> Dict:
    if event_type in ("created", "modified"):
        if file_content is None:
            return {"status": "skipped", "reason": "no file content provided"}

        text, err = extract_text_from_bytes(file_content, os.path.basename(file_path))
        if err or not text.strip():
            log_watch_event(client_id, event_type, file_path, old_path)
            return {"status": "skipped", "reason": err or "empty text"}

        title = os.path.basename(file_path).rsplit(".", 1)[0]
        lang = _classify_lang(text)

        # Upload extracted text to S3
        s3_key = f"{uuid.uuid4().hex[:12]}.txt"
        try:
            s3_client.upload_text(text, s3_key)
        except Exception:
            s3_key = None

        doc_langs = get_all_document_texts_with_lang()
        all_texts = [d[0] for d in doc_langs] + [text]
        all_langs = [d[1] for d in doc_langs] + [lang]
        expand_vocabulary([text], all_texts,
                          load_vocabulary, load_idf, save_vocabulary, save_idf,
                          lang=lang)
        _reembed_all()

        summary = generate_summary(text, lang=lang)
        embedding = vectorize_text_with_dim(text, vector_dim, lang)
        doc_id = upsert_document(title, text, embedding, summary, file_path, lang=lang, s3_key=s3_key)

        log_watch_event(client_id, event_type, file_path, old_path)
        return {"status": "indexed", "document_id": doc_id, "title": title, "lang": lang}

    if event_type == "deleted":
        deleted = delete_document_by_path(file_path)
        if deleted:
            _rebuild_vocab_idf()
        log_watch_event(client_id, event_type, file_path, old_path)
        return {"status": "deleted" if deleted else "not_found"}

    return {"status": "unknown_event", "event_type": event_type}
