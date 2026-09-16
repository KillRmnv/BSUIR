from flask import Blueprint, request, jsonify, Response
from services import translation_service
from services.errors import ValidationError

translate_bp = Blueprint("translate", __name__)


@translate_bp.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": e.message}), e.status_code


@translate_bp.errorhandler(Exception)
def handle_generic(e):
    return jsonify({"error": "Internal server error"}), 500


@translate_bp.route("/api/translate", methods=["POST"])
def api_translate():
    data = request.get_json(force=True)
    return jsonify(translation_service.translate(data.get("text", "").strip()))


@translate_bp.route("/api/translate-nmt", methods=["POST"])
def api_translate_nmt():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    if not text:
        raise ValidationError("text is required")
    from translator.nmt_engine import translate_text
    return jsonify(translate_text(text))


@translate_bp.route("/api/translate/pos", methods=["POST"])
def api_translate_pos():
    data = request.get_json(force=True)
    return jsonify(translation_service.pos_tag(
        text=data.get("text", "").strip(),
        lang=data.get("lang", "en"),
    ))


@translate_bp.route("/api/translate/parse", methods=["POST"])
def api_translate_parse():
    data = request.get_json(force=True)
    return jsonify(translation_service.syntax_parse(
        text=data.get("text", "").strip(),
        lang=data.get("lang", "en"),
    ))


@translate_bp.route("/api/translate/dict", methods=["GET"])
def api_translate_dict_list():
    return jsonify(translation_service.dict_list(
        limit=int(request.args.get("limit", 100)),
        offset=int(request.args.get("offset", 0)),
    ))


@translate_bp.route("/api/translate/dict", methods=["POST"])
def api_translate_dict_add():
    data = request.get_json(force=True)
    return jsonify(translation_service.dict_add(
        source=data.get("source", "").strip(),
        target=data.get("target", "").strip(),
        source_pos=data.get("source_pos", ""),
        target_pos=data.get("target_pos", ""),
    ))


@translate_bp.route("/api/translate/dict/search", methods=["GET"])
def api_translate_dict_search():
    return jsonify(translation_service.dict_search(request.args.get("q", "").strip()))


@translate_bp.route("/api/translate/dict/bulk", methods=["POST"])
def api_translate_dict_bulk():
    data = request.get_json(force=True)
    return jsonify(translation_service.dict_bulk_add(data.get("entries", [])))


@translate_bp.route("/api/translate/dict/bootstrap", methods=["POST"])
def api_translate_dict_bootstrap():
    return jsonify(translation_service.dict_bootstrap())


@translate_bp.route("/api/translate/dict/delete", methods=["POST"])
def api_translate_dict_delete():
    data = request.get_json(force=True)
    return jsonify(translation_service.dict_delete(data.get("id")))


@translate_bp.route("/api/translate/freq", methods=["POST"])
def api_translate_freq():
    data = request.get_json(force=True)
    return jsonify(translation_service.frequency_list(data.get("text", "").strip()))


@translate_bp.route("/api/translate/export", methods=["POST"])
def api_translate_export():
    data = request.get_json(force=True)
    result = translation_service.export_txt(
        text=data.get("text", "").strip(),
        filename=data.get("filename", "translation.txt"),
    )
    return Response(
        result["content"],
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={result['filename']}"},
    )
