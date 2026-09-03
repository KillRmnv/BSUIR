import os
import glob
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from database_manager import (
    init_db,
    get_all_documents,
    get_document_by_id,
    delete_document,
    get_document_count,
    load_vocabulary,
    load_idf,
    save_vocabulary,
    save_idf,
)
from search_engine import SearchEngine
from evaluator import calculate_metrics, evaluate_search_results, plot_metrics
from document_processor import vectorize_text_with_dim, build_vocabulary, compute_idf, get_query_terms, highlight_terms
from document_loader import extract_text_from_bytes
import document_processor as dp

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

engine = SearchEngine(vector_dim=1000)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json()
    query = data.get("query", "")
    top_k = data.get("top_k", 10)
    if not query.strip():
        return jsonify({"error": "Query is empty"}), 400
    result = engine.get_results(query, top_k)
    return jsonify(result)


@app.route("/api/upload", methods=["POST"])
def api_upload():
    data = request.get_json()
    title = data.get("title", "")
    content = data.get("content", "")
    if not title.strip() or not content.strip():
        return jsonify({"error": "Title and content are required"}), 400

    docs = get_all_documents()
    all_texts = [d["content"] for d in docs] + [content]
    build_vocabulary(all_texts)
    compute_idf(all_texts)
    save_vocabulary(dp.VOCAB)
    save_idf(dp.IDF)

    indexed = engine.index_documents([{"title": title, "content": content}])
    return jsonify({"message": "Document indexed", "count": indexed})


@app.route("/api/upload-file", methods=["POST"])
def api_upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    content, error = extract_text_from_bytes(file.read(), file.filename)
    if error:
        return jsonify({"error": error}), 400
    if not content.strip():
        return jsonify({"error": "No text could be extracted from this file"}), 400

    title = file.filename.rsplit(".", 1)[0] if "." in file.filename else file.filename

    docs = get_all_documents()
    all_texts = [d["content"] for d in docs] + [content]
    build_vocabulary(all_texts)
    compute_idf(all_texts)
    save_vocabulary(dp.VOCAB)
    save_idf(dp.IDF)

    indexed = engine.index_documents([{"title": title, "content": content}])
    return jsonify({"message": "File uploaded and indexed", "count": indexed, "title": title})


@app.route("/api/documents", methods=["GET"])
def api_documents():
    docs = get_all_documents()
    return jsonify({"documents": docs, "total": len(docs)})


@app.route("/api/documents/<int:doc_id>", methods=["GET"])
def api_document_detail(doc_id):
    doc = get_document_by_id(doc_id)
    if not doc:
        return jsonify({"error": "Document not found"}), 404
    query = request.args.get("query", "")
    if query.strip():
        terms = set(get_query_terms(query))
        if terms:
            highlighted, matched = highlight_terms(doc["content"], terms)
            doc["highlighted_content"] = highlighted
            doc["matched_terms"] = matched
    return jsonify(doc)


@app.route("/api/documents/<int:doc_id>", methods=["DELETE"])
def api_delete_document(doc_id):
    deleted = delete_document(doc_id)
    if not deleted:
        return jsonify({"error": "Document not found"}), 404
    return jsonify({"message": "Document deleted"})


@app.route("/api/metrics", methods=["POST"])
def api_metrics():
    data = request.get_json()
    queries_results = data.get("queries_results", [])
    if not queries_results:
        return jsonify({"error": "No evaluation data provided"}), 400

    # Backward compatibility: if a query entry has no retrieved_ids,
    # run the live search to obtain them
    for qr in queries_results:
        if "retrieved_ids" not in qr and qr.get("query"):
            res = engine.get_results(qr["query"], top_k=10)
            qr["retrieved_ids"] = [r["id"] for r in res.get("results", [])]

    evaluation = evaluate_search_results(queries_results)
    chart_b64 = plot_metrics(evaluation)
    evaluation["chart"] = chart_b64
    return jsonify(evaluation)


@app.route("/api/stats", methods=["GET"])
def api_stats():
    count = get_document_count()
    return jsonify({"document_count": count})


@app.route("/api/help", methods=["GET"])
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


@app.route("/api/init-db", methods=["POST"])
def api_init_db():
    init_db()
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    txt_files = glob.glob(os.path.join(docs_dir, "*.txt"))
    if txt_files:
        texts = []
        for f in txt_files:
            with open(f, "r", encoding="utf-8") as fh:
                texts.append(fh.read())
        build_vocabulary(texts)
        compute_idf(texts)
        save_vocabulary(dp.VOCAB)
        save_idf(dp.IDF)
        for f in txt_files:
            with open(f, "r", encoding="utf-8") as fh:
                content = fh.read()
            title = os.path.basename(f).rsplit(".", 1)[0]
            engine.index_documents([{"title": title, "content": content}])
    return jsonify({"message": "Database initialized", "documents_loaded": len(txt_files)})


if __name__ == "__main__":
    if not dp.VOCAB:
        saved_vocab = load_vocabulary()
        saved_idf = load_idf()
        if saved_vocab and saved_idf:
            dp.VOCAB = saved_vocab
            dp.IDF = saved_idf
        else:
            docs = get_all_documents()
            if docs:
                all_texts = [d["content"] for d in docs]
                build_vocabulary(all_texts)
                compute_idf(all_texts)
                save_vocabulary(dp.VOCAB)
                save_idf(dp.IDF)
    app.run(host="0.0.0.0", port=5000, debug=False)
