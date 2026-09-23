from flask import Blueprint, request, jsonify, current_app

from services import stt_service
from services.errors import ValidationError, ServiceError

stt_bp = Blueprint("stt", __name__)


@stt_bp.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": e.message}), e.status_code


@stt_bp.errorhandler(ServiceError)
def handle_service(e):
    return jsonify({"error": e.message}), e.status_code


@stt_bp.errorhandler(Exception)
def handle_generic(e):
    return jsonify({"error": "Internal server error"}), 500


@stt_bp.route("/api/stt/status", methods=["GET"])
def api_stt_status():
    return jsonify(stt_service.status())


@stt_bp.route("/api/stt/commands", methods=["GET"])
def api_stt_commands():
    return jsonify(stt_service.list_commands())


@stt_bp.route("/api/stt/commands", methods=["POST"])
def api_stt_commands_save():
    data = request.get_json(force=True)
    return jsonify(stt_service.update_commands(data))


@stt_bp.route("/api/stt/commands/reset", methods=["POST"])
def api_stt_commands_reset():
    return jsonify(stt_service.reset_commands())


@stt_bp.route("/api/stt/recognize", methods=["POST"])
def api_stt_recognize():
    lang = request.form.get("lang", request.args.get("lang", "en"))
    doc_id = request.form.get("doc_id") or request.args.get("doc_id")
    wav = b""
    if "wav" in request.files:
        wav = request.files["wav"].read()
    elif request.files:
        wav = next(iter(request.files.values())).read()
    engine = current_app.config.get("ENGINE")
    result = stt_service.recognize(wav, lang=lang, doc_id=doc_id, engine=engine)
    return jsonify(result)
