from flask import Blueprint, request, jsonify, current_app
from services import watcher_service
from services.errors import ValidationError

watcher_bp = Blueprint("watcher", __name__)


def _get_engine():
    return current_app.config["ENGINE"]


@watcher_bp.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": e.message}), e.status_code


@watcher_bp.errorhandler(Exception)
def handle_generic(e):
    return jsonify({"error": "Internal server error"}), 500


@watcher_bp.route("/api/watch-event", methods=["POST"])
def api_watch_event():
    data = request.get_json(force=True) or {}
    result = watcher_service.process_watch_event(data, _get_engine().vector_dim)
    return jsonify(result)


@watcher_bp.route("/api/watch-clients", methods=["GET", "POST"])
def api_watch_clients():
    if request.method == "POST":
        data = request.get_json(force=True) or {}
        result = watcher_service.register_client(
            data.get("client_id", ""),
            data.get("watched_dir", ""),
        )
        return jsonify(result)
    return jsonify(watcher_service.list_clients())
