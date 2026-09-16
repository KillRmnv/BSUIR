from flask import Blueprint, request, jsonify
from services import summarization_service
from services.errors import ValidationError, NotFoundError

summarize_bp = Blueprint("summarize", __name__)


@summarize_bp.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": e.message}), e.status_code


@summarize_bp.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({"error": e.message}), e.status_code


@summarize_bp.errorhandler(Exception)
def handle_generic(e):
    return jsonify({"error": "Internal server error"}), 500


@summarize_bp.route("/api/summarize", methods=["POST"])
def api_summarize():
    data = request.get_json(force=True)
    result = summarization_service.summarize_text(
        text=data.get("text", "").strip(),
        method=data.get("method", "textrank"),
        n_sentences=int(data.get("n_sentences", 10)),
        lang=data.get("lang", "en"),
    )
    return jsonify(result)


@summarize_bp.route("/api/summarize-doc", methods=["POST"])
def api_summarize_doc():
    data = request.get_json(force=True)
    result = summarization_service.summarize_document(
        doc_id=data.get("doc_id"),
        method=data.get("method", "textrank"),
        n_sentences=int(data.get("n_sentences", 10)),
    )
    return jsonify(result)
