from flask import Blueprint, request, jsonify, current_app, send_file
from services import document_service
from services.errors import ValidationError, NotFoundError
import io

documents_bp = Blueprint("documents", __name__)


def _get_engine():
    return current_app.config["ENGINE"]


@documents_bp.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": e.message}), e.status_code


@documents_bp.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({"error": e.message}), e.status_code


@documents_bp.errorhandler(Exception)
def handle_generic(e):
    return jsonify({"error": "Internal server error"}), 500


@documents_bp.route("/api/documents", methods=["GET"])
def api_documents():
    return jsonify(document_service.list_documents())


@documents_bp.route("/api/documents/<int:doc_id>", methods=["GET"])
def api_document_detail(doc_id):
    query = request.args.get("query", "")
    return jsonify(document_service.get_document(doc_id, query))


@documents_bp.route("/api/documents/<int:doc_id>", methods=["DELETE"])
def api_delete_document(doc_id):
    document_service.remove_document(doc_id)
    return jsonify({"message": "Document deleted"})


@documents_bp.route("/api/documents/<int:doc_id>/download", methods=["GET"])
def api_download_document(doc_id):
    doc = document_service.get_document(doc_id)
    if not doc:
        return jsonify({"error": "Document not found"}), 404
    s3_key = doc.get("s3_key")
    if s3_key:
        from storage import s3_client
        file_bytes = s3_client.download_file(s3_key)
        if file_bytes:
            title = doc.get("title", "document")
            ext = s3_key.rsplit(".", 1)[-1] if "." in s3_key else "bin"
            mime_map = {
                "txt": "text/plain",
                "pdf": "application/pdf",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "html": "text/html",
                "htm": "text/html",
                "csv": "text/csv",
                "json": "application/json",
                "xml": "application/xml",
                "md": "text/markdown",
            }
            mime = mime_map.get(ext.lower(), "application/octet-stream")
            buf = io.BytesIO(file_bytes)
            buf.seek(0)
            return send_file(buf, mimetype=mime, as_attachment=True,
                             download_name=f"{title}.{ext}")
    content = doc.get("content", "")
    title = doc.get("title", "document")
    buf = io.BytesIO(content.encode("utf-8"))
    buf.seek(0)
    return send_file(buf, mimetype="text/plain", as_attachment=True,
                     download_name=f"{title}.txt")


@documents_bp.route("/api/upload", methods=["POST"])
def api_upload():
    data = request.get_json()
    result = document_service.upload_text(
        data.get("title", ""),
        data.get("content", ""),
        _get_engine(),
    )
    return jsonify(result)


@documents_bp.route("/api/upload-file", methods=["POST"])
def api_upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    result = document_service.upload_file(request.files["file"], _get_engine())
    return jsonify(result)
