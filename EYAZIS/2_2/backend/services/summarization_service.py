from summarizer.summary_engine import summarize
from data.database_manager import get_document_by_id
from services.errors import ValidationError, NotFoundError


def summarize_text(text: str, method: str = "textrank",
                   n_sentences: int = 10, lang: str = "en") -> dict:
    if not text:
        raise ValidationError("text is required")
    if method not in ("extraction", "textrank"):
        raise ValidationError("method must be 'extraction' or 'textrank'")
    return summarize(text, method=method, n_sentences=n_sentences, lang=lang)


def summarize_document(doc_id, method: str = "textrank",
                       n_sentences: int = 10) -> dict:
    if not doc_id:
        raise ValidationError("doc_id is required")
    doc = get_document_by_id(doc_id)
    if not doc:
        raise NotFoundError("Document not found")
    result = summarize(doc["content"], method=method, n_sentences=n_sentences,
                       lang=doc.get("lang", "en"))
    result["doc_id"] = doc_id
    result["title"] = doc.get("title", "")
    return result
