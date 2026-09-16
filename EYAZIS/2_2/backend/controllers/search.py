from flask import Blueprint, request, jsonify, current_app
from services import search_service
from services.errors import ValidationError

search_bp = Blueprint("search", __name__)


def _get_engine():
    return current_app.config["ENGINE"]


@search_bp.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": e.message}), e.status_code


@search_bp.errorhandler(Exception)
def handle_generic(e):
    return jsonify({"error": "Internal server error"}), 500


@search_bp.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json()
    query = data.get("query", "")
    top_k = data.get("top_k", 10)
    if not query.strip():
        return jsonify({"error": "Query is empty"}), 400
    result = search_service.search_documents(_get_engine(), query, top_k)
    return jsonify(result)


@search_bp.route("/api/metrics", methods=["POST"])
def api_metrics():
    data = request.get_json()
    queries_results = data.get("queries_results", [])
    if not queries_results:
        return jsonify({"error": "No evaluation data provided"}), 400
    evaluation = search_service.get_metrics(_get_engine(), queries_results)
    return jsonify(evaluation)


@search_bp.route("/api/stats", methods=["GET"])
def api_stats():
    return jsonify(search_service.get_stats())
