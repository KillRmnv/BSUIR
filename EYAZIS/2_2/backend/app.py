import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from search.search_engine import SearchEngine
from search import document_processor as dp
from data.database_manager import load_vocabulary, load_idf
from services.init_service import ensure_corpus, ensure_lang_model
from storage.s3_client import ensure_bucket
from controllers import (
    search_bp, documents_bp, lang_bp, summarize_bp,
    translate_bp, tts_bp, stt_bp, watcher_bp, admin_bp,
)
from services.errors import AppError


def create_app():
    app = Flask(__name__, static_folder="frontend", static_url_path="")
    CORS(app)

    engine = SearchEngine(vector_dim=5000)
    app.config["ENGINE"] = engine

    # Register blueprints
    app.register_blueprint(search_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(lang_bp)
    app.register_blueprint(summarize_bp)
    app.register_blueprint(translate_bp)
    app.register_blueprint(tts_bp)
    app.register_blueprint(stt_bp)
    app.register_blueprint(watcher_bp)
    app.register_blueprint(admin_bp)

    # Global error handlers
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return jsonify({"error": e.message}), e.status_code

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def handle_internal(e):
        return jsonify({"error": "Internal server error"}), 500

    # Static file serving
    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        return send_from_directory(app.static_folder, path)

    return app


if __name__ == "__main__":
    app = create_app()
    engine = app.config["ENGINE"]
    try:
        ensure_bucket()
    except Exception:
        pass

    if not dp.VOCAB:
        saved_vocab = load_vocabulary()
        saved_idf = load_idf()
        if saved_vocab and saved_idf:
            dp.VOCAB = saved_vocab
            dp.IDF = saved_idf

    base_dir = os.path.dirname(__file__)
    ensure_corpus(engine, base_dir)
    ensure_lang_model(base_dir)

    app.run(host="0.0.0.0", port=5000, debug=False)
