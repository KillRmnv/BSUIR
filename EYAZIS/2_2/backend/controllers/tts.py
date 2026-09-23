from flask import Blueprint, request, jsonify, Response

from services import tts_service
from services.errors import ValidationError, ServiceError

tts_bp = Blueprint("tts", __name__)


@tts_bp.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": e.message}), e.status_code


@tts_bp.errorhandler(ServiceError)
def handle_service(e):
    return jsonify({"error": e.message}), e.status_code


@tts_bp.errorhandler(Exception)
def handle_generic(e):
    return jsonify({"error": "Internal server error"}), 500


@tts_bp.route("/api/tts/status", methods=["GET"])
def api_tts_status():
    return jsonify(tts_service.status())


@tts_bp.route("/api/tts/voices", methods=["GET"])
def api_tts_voices():
    return jsonify(tts_service.list_voices())


@tts_bp.route("/api/tts/detect-lang", methods=["POST"])
def api_tts_detect_lang():
    data = request.get_json(force=True)
    return jsonify(tts_service.detect_lang(data.get("text", "")))


@tts_bp.route("/api/tts/synthesize", methods=["POST"])
def api_tts_synthesize():
    data = request.get_json(force=True)
    result = tts_service.synthesize(
        text=data.get("text", ""),
        voice_id=data.get("voice"),
        lang=data.get("lang"),
        rate=data.get("rate", 1.0),
        volume=data.get("volume", 100),
        pitch=data.get("pitch", 50),
        engine=data.get("engine"),
    )
    audio = result.pop("audio")
    headers = {
        "X-TTS-Voice": result["voice"],
        "X-TTS-Engine": result["engine"],
        "X-TTS-Lang": result["lang"],
        "X-TTS-Elapsed-Ms": str(result["elapsed_ms"]),
        "X-TTS-Duration-S": str(result["duration_s"]),
        "X-TTS-Chars": str(result["chars"]),
        "X-TTS-Normalized": result["normalized"],
        "Content-Disposition": "inline; filename=tts.wav",
    }
    return Response(audio, mimetype="audio/wav", headers=headers)
