from typing import List, Dict, Optional
from search.document_processor import (
    clean_text,
    vectorize_text_with_dim,
    build_vocabulary,
    compute_idf,
    get_vocab_size,
    extract_keywords,
    get_query_terms,
    highlight_snippet,
    generate_summary,
    VOCAB,
    IDF,
)
from search import document_processor as dp
from data.database_manager import search_documents, log_search, load_vocabulary, load_idf, insert_document, get_all_document_texts_with_lang
from lang_detection.lang_ngram import classify_text


class SearchEngine:
    def __init__(self, vector_dim: int = 5000):
        self.vector_dim = vector_dim

    def _ensure_vocab(self) -> bool:
        if not dp.VOCAB:
            saved_vocab = load_vocabulary()
            saved_idf = load_idf()
            if saved_vocab and saved_idf:
                dp.VOCAB = saved_vocab
                dp.IDF = saved_idf
                return True
            return False
        return True

    def _detect_lang(self, text: str) -> str:
        """Lightweight query language detection using ngram method."""
        try:
            result = classify_text(text)
            return result.get("lang", "en")
        except Exception:
            return "en"

    def process_query(self, query_string: str, lang: str = 'en') -> List[float]:
        return vectorize_text_with_dim(query_string, self.vector_dim, lang)

    def get_results(self, query_string: str, top_k: int = 10) -> Dict:
        if not self._ensure_vocab():
            return {"error": "Vocabulary not initialized. Call /api/init-db first.", "query": query_string, "keywords": [], "results": [], "total_found": 0}

        detected = self._detect_lang(query_string)
        order = [detected, "fr" if detected == "en" else "en"]
        if not any(v in query_string.lower() for v in "éèêëàâçîïôöùûüœ") and detected == "fr" and len(query_string.split()) == 1:
            order = ["en", "fr"]
        best = None
        for query_lang in order:
            query_vector = self.process_query(query_string, query_lang)
            if not any(query_vector):
                continue
            raw_results = search_documents(query_vector, top_k)
            raw_results = [
                r for r in raw_results
                if r["similarity"] is not None and r["similarity"] == r["similarity"] and r["similarity"] > 0
            ]
            if raw_results or best is None:
                best = {
                    "query_lang": query_lang,
                    "query_vector": query_vector,
                    "raw_results": raw_results,
                }
            if raw_results:
                break

        if best is None:
            return {
                "query": query_string,
                "query_lang": detected,
                "keywords": [],
                "results": [],
                "total_found": 0,
                "note": "query_out_of_vocabulary",
            }

        query_lang = best["query_lang"]
        log_search(query_string, best["query_vector"])
        raw_results = best["raw_results"]
        keywords = extract_keywords(query_string, lang=query_lang)
        query_terms = set(get_query_terms(query_string, query_lang))

        for res in raw_results:
            doc_lang = res.get("lang", "en")
            snippet_html, matched = highlight_snippet(res["content"], query_terms, lang=doc_lang)
            if not matched:
                doc_terms = set(extract_keywords(res["content"], 5, lang=doc_lang))
                snippet_html, matched = highlight_snippet(res["content"], doc_terms, lang=doc_lang)
            res["highlighted_content"] = snippet_html
            res["matched_terms"] = matched

        return {
            "query": query_string,
            "query_lang": query_lang,
            "keywords": keywords,
            "results": raw_results,
            "total_found": len(raw_results),
        }

    def index_documents(self, documents: List[Dict[str, str]]) -> int:
        indexed = 0
        for doc in documents:
            doc_lang = doc.get("lang", "en")
            embedding = vectorize_text_with_dim(doc["content"], self.vector_dim, doc_lang)
            summary = generate_summary(doc["content"], lang=doc_lang)
            insert_document(
                doc["title"],
                doc["content"],
                embedding,
                summary=summary,
                file_path=doc.get("file_path"),
                lang=doc_lang,
                s3_key=doc.get("s3_key"),
            )
            indexed += 1
        return indexed

    def update_vocab_from_db(self, documents: List[Dict[str, str]]):
        doc_langs = get_all_document_texts_with_lang()
        if doc_langs:
            texts = [d[0] for d in doc_langs]
            langs = [d[1] for d in doc_langs]
            build_vocabulary(texts, langs=langs)
            compute_idf(texts, langs=langs)
