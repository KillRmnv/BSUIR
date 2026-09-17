import os
import uuid
from data.database_manager import (
    get_all_documents,
    get_document_by_id,
    delete_document,
    get_all_document_ids_and_contents,
    get_all_document_texts_with_lang,
    update_document_embedding,
    load_vocabulary,
    load_idf,
    save_vocabulary,
    save_idf,
)
from search.document_processor import (
    vectorize_text_with_dim,
    expand_vocabulary,
    get_query_terms,
    highlight_terms,
)
from search import document_processor as dp
from doc_loader.document_loader import extract_text_from_bytes
from services.errors import ValidationError, NotFoundError
from storage import s3_client
from lang_detection.lang_methods import classify_text_all


def _classify_lang(text: str) -> str:
    try:
        result = classify_text_all(text)
        return result.get("lang", "en")
    except Exception:
        return "en"


def _rebuild_embeddings(engine):
    all_docs = get_all_document_ids_and_contents()
    for doc in all_docs:
        emb = vectorize_text_with_dim(doc["content"], engine.vector_dim, doc.get("lang", "en"))
        update_document_embedding(doc["id"], emb)


def _expand_and_reembed(content: str, lang: str, engine):
    doc_langs = get_all_document_texts_with_lang()
    existing_texts = [d[0] for d in doc_langs]
    all_texts = existing_texts + [content]
    expand_vocabulary([content], all_texts,
                      load_vocabulary, load_idf, save_vocabulary, save_idf,
                      lang=lang)
    _rebuild_embeddings(engine)


def upload_text(title: str, content: str, engine) -> dict:
    if not title.strip() or not content.strip():
        raise ValidationError("Title and content are required")
    lang = _classify_lang(content)
    _expand_and_reembed(content, lang, engine)
    indexed = engine.index_documents([{"title": title, "content": content, "lang": lang}])
    return {"message": "Document indexed", "count": indexed, "lang": lang}


def upload_file(file_storage, engine) -> dict:
    if file_storage.filename == "":
        raise ValidationError("No file selected")
    file_bytes = file_storage.read()
    content, error = extract_text_from_bytes(file_bytes, file_storage.filename)
    if error:
        raise ValidationError(error)
    if not content.strip():
        raise ValidationError("No text could be extracted from this file")
    title = file_storage.filename.rsplit(".", 1)[0] if "." in file_storage.filename else file_storage.filename

    # Upload text to S3
    s3_key = f"{uuid.uuid4().hex[:12]}.txt"
    try:
        s3_client.upload_text(content, s3_key)
    except Exception:
        s3_key = None

    lang = _classify_lang(content)
    _expand_and_reembed(content, lang, engine)
    indexed = engine.index_documents([{"title": title, "content": content, "lang": lang, "s3_key": s3_key}])
    return {"message": "File uploaded and indexed", "count": indexed, "title": title, "lang": lang}


def list_documents() -> dict:
    docs = get_all_documents()
    return {"documents": docs, "total": len(docs)}


def get_document(doc_id: int, query: str = "") -> dict:
    doc = get_document_by_id(doc_id)
    if not doc:
        raise NotFoundError("Document not found")
    if query.strip() and doc.get("content"):
        terms = set(get_query_terms(query))
        if terms:
            highlighted, matched = highlight_terms(doc["content"], terms)
            doc["highlighted_content"] = highlighted
            doc["matched_terms"] = matched
    return doc


def remove_document(doc_id: int) -> None:
    deleted = delete_document(doc_id)
    if not deleted:
        raise NotFoundError("Document not found")
