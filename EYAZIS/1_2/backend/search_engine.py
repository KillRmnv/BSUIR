from typing import List, Dict
from document_processor import (
    clean_text,
    vectorize_text_with_dim,
    build_vocabulary,
    compute_idf,
    get_vocab_size,
    extract_keywords,
    get_query_terms,
    highlight_snippet,
    VOCAB,
    IDF,
)
import document_processor as dp
from database_manager import search_documents, log_search, load_vocabulary, load_idf


class SearchEngine:
    def __init__(self, vector_dim: int = 1000):
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

    def process_query(self, query_string: str) -> List[float]:
        return vectorize_text_with_dim(query_string, self.vector_dim)

    def get_results(self, query_string: str, top_k: int = 10) -> Dict:
        if not self._ensure_vocab():
            return {"error": "Vocabulary not initialized. Call /api/init-db first.", "query": query_string, "keywords": [], "results": [], "total_found": 0}

        query_vector = self.process_query(query_string)
        log_search(query_string, query_vector)
        raw_results = search_documents(query_vector, top_k)
        # Drop results with zero similarity — they add no value
        raw_results = [r for r in raw_results if r["similarity"] > 0]
        keywords = extract_keywords(query_string)
        query_terms = set(get_query_terms(query_string))

        for res in raw_results:
            snippet_html, matched = highlight_snippet(res["content"], query_terms)
            if not matched:
                # No query term in this doc — fall back to the doc's own top TF-IDF keywords
                doc_terms = set(extract_keywords(res["content"], 5))
                snippet_html, matched = highlight_snippet(res["content"], doc_terms)
            res["highlighted_content"] = snippet_html
            res["matched_terms"] = matched

        return {
            "query": query_string,
            "keywords": keywords,
            "results": raw_results,
            "total_found": len(raw_results),
        }

    def index_documents(self, documents: List[Dict[str, str]]) -> int:
        from database_manager import insert_document

        indexed = 0
        for doc in documents:
            embedding = vectorize_text_with_dim(doc["content"], self.vector_dim)
            insert_document(doc["title"], doc["content"], embedding)
            indexed += 1
        return indexed

    def update_vocab_from_db(self, documents: List[Dict[str, str]]):
        texts = [doc["content"] for doc in documents]
        if texts:
            build_vocabulary(texts)
            compute_idf(texts)
