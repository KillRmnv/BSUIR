import os
from flask import Blueprint, request, jsonify, current_app
from services import lang_service
from services.errors import ValidationError, ServiceError

lang_bp = Blueprint("lang", __name__)


@lang_bp.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": e.message}), e.status_code


@lang_bp.errorhandler(ServiceError)
def handle_service(e):
    return jsonify({"error": e.message}), e.status_code


@lang_bp.errorhandler(Exception)
def handle_generic(e):
    return jsonify({"error": "Internal server error"}), 500


@lang_bp.route("/api/lang/status", methods=["GET"])
def api_lang_status():
    try:
        return jsonify(lang_service.status())
    except Exception as e:
        return jsonify({"trained": False, "error": str(e)}), 500


@lang_bp.route("/api/lang/train", methods=["POST"])
def api_lang_train():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    try:
        result = lang_service.train(base_dir)
    except ValidationError as e:
        return jsonify({"error": e.message}), 400
    except (RuntimeError, ValueError) as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(result)


@lang_bp.route("/api/lang/classify", methods=["POST"])
def api_lang_classify():
    try:
        if "file" in request.files and request.files["file"].filename:
            result = lang_service.classify_file(request.files["file"])
            return jsonify(result)
        data = request.get_json(force=True, silent=True) or {}
        text = data.get("text", "")
        if not text.strip():
            return jsonify({"error": "Provide a file or JSON {text}"}), 400
        result = lang_service.classify_text(text)
        return jsonify(result)
    except (FileNotFoundError, RuntimeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@lang_bp.route("/api/lang/classify-batch", methods=["POST"])
def api_lang_classify_batch():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    try:
        return jsonify(lang_service.classify_batch(base_dir))
    except ValidationError as e:
        return jsonify({"error": e.message}), 400
    except (FileNotFoundError, RuntimeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
