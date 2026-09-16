import os
from flask import Blueprint, request, jsonify, current_app
from services import init_service

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/api/init-db", methods=["POST"])
def api_init_db():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    result = init_service.initialize_corpus(current_app.config["ENGINE"], base_dir)
    return jsonify(result)


@admin_bp.route("/api/help", methods=["GET"])
def api_help():
    return jsonify({
        "theoretical_terms": {
            "tf_idf": {
                "term": "TF-IDF (Term Frequency-Inverse Document Frequency)",
                "definition": "A numerical statistic that reflects how important a word is to a document in a collection. TF measures word frequency in a document, IDF measures how rare a word is across all documents.",
                "formula": "TF-IDF(t,d) = TF(t,d) * IDF(t)",
            },
            "cosine_similarity": {
                "term": "Cosine Similarity",
                "definition": "A metric used to measure how similar two vectors are irrespective of their size. It calculates the cosine of the angle between two vectors projected in a multi-dimensional space.",
                "formula": "similarity = (A . B) / (||A|| * ||B||)",
            },
            "vector_space_model": {
                "term": "Vector Space Model",
                "definition": "An algebraic model for representing text documents as vectors of identifiers, such as terms. Each dimension corresponds to a separate term, and the value represents the weight of that term in the document.",
            },
            "pgvector": {
                "term": "pgvector",
                "definition": "An open-source PostgreSQL extension that enables storing and searching over machine learning-generated vector embeddings. Supports exact and approximate nearest neighbor search.",
            },
            "precision": {
                "term": "Precision",
                "definition": "The fraction of retrieved documents that are relevant to the query. Measures the accuracy of the search results.",
                "formula": "Precision = |retrieved AND relevant| / |retrieved|",
            },
            "recall": {
                "term": "Recall",
                "definition": "The fraction of relevant documents that were successfully retrieved. Measures the completeness of the search results.",
                "formula": "Recall = |retrieved AND relevant| / |relevant|",
            },
            "fscore": {
                "term": "F-Score",
                "definition": "The harmonic mean of precision and recall, providing a single metric that balances both concerns.",
                "formula": "F1 = 2 * (precision * recall) / (precision + recall)",
            },
            "lemmatization": {
                "term": "Lemmatization",
                "definition": "The process of reducing words to their base or dictionary form (lemma), considering the context and meaning of the word.",
            },
            "stop_words": {
                "term": "Stop Words",
                "definition": "Common words (like 'the', 'is', 'at') that are filtered out before text processing because they carry little meaningful information.",
            },
            "stemming": {
                "term": "Stemming",
                "definition": "The process of reducing inflected words to their word stem by removing prefixes and suffixes using heuristic rules.",
            },
        },
        "navigation": {
            "home": "Main page with the search bar. Enter your query to search through the document corpus.",
            "search_results": "After searching, results are displayed with similarity scores. Click on any document to view its full content.",
            "upload": "Upload documents to the corpus. You can enter text manually or upload files: .txt, .md, .pdf, .docx, .html, .rtf, .csv, .log.",
            "metrics": "View evaluation metrics (Precision, Recall, F-Score) for search quality analysis.",
            "documents": "Browse all indexed documents in the corpus with their metadata.",
            "help": "This page. Contains theoretical background and navigation guide.",
        },
    })
