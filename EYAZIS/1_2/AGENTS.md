# AGENTS.md — EYAZIS/1_2 (IR System)

## What this is

Flask + PostgreSQL (pgvector) information retrieval system with TF-IDF vectorization. Vanilla JS frontend served by Flask. Dockerized.

## Quick start

```bash
docker-compose up --build
```

App at `http://localhost:5000`. After DB is healthy, initialize the corpus:

```bash
curl -X POST http://localhost:5000/api/init-db
```

## Architecture

- `backend/app.py` — Flask entry point, serves API + static frontend
- `backend/document_processor.py` — TF-IDF vectorization, text cleaning, vocabulary building, token highlighting (`highlight_snippet`)
- `backend/document_loader.py` — file upload strategy: extracts text from .txt/.md/.pdf/.docx/.html/.rtf/.csv/.log by extension
- `backend/search_engine.py` — Search orchestration (vectorize query → pgvector similarity search), builds highlighted snippets per result
- `backend/database_manager.py` — All PostgreSQL operations (CRUD, vector search via `<=>` operator)
- `backend/migrate.py` — Custom migration runner (reads `backend/migrations/*.sql`, tracks in `schema_migrations` table)
- `backend/migrations/001_init.sql` — Creates pgvector extension + `documents`, `search_logs`, `schema_migrations` tables
- `frontend/` — Static HTML/JS/CSS, no build step

## Key constraints

- Vector dimension is **1000** — hardcoded in `app.py:20` (`SearchEngine(vector_dim=1000)`) and `migrations/001_init.sql:14` (`vector(1000)`). Changing one requires changing the other.
- NLTK data (`stopwords`, `punkt`) downloaded at Docker build time in `Dockerfile:11`.
- DB credentials in `docker-compose.yml` (`ir_user` / `ir_password` / `ir_system`). App reads them via env vars with localhost defaults.
- Vocabulary and IDF are **in-memory globals** in `document_processor.py` (`VOCAB`, `IDF`). They must be rebuilt on startup or after uploads by calling `build_vocabulary()` and `compute_idf()`. The `/api/init-db` and `/api/upload` endpoints do this automatically.
- `pgdata/` volume persists DB data locally — listed in `.gitignore`.

## API endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/init-db` | Run migrations + load `backend/documents/*.txt` |
| POST | `/api/search` | Vector search (`{query, top_k}`) |
| POST | `/api/upload` | Index a document (`{title, content}`) |
| POST | `/api/upload-file` | Upload a file (.txt/.md/.pdf/.docx/.html/.rtf/.csv/.log — text extracted via `document_loader.py`) |
| GET | `/api/documents` | List all documents |
| DELETE | `/api/documents/<id>` | Delete a document |
| POST | `/api/metrics` | Evaluate search quality (precision/recall/F1) |
| GET | `/api/stats` | Document count |

## Gotchas

- No test suite, no linter, no formatter configured. Verify changes by running the app and testing manually.
- Flask serves frontend as static files (`static_folder="frontend"`). HTML pages reference JS via relative paths — no bundling.
- Search results: `search_documents` returns the **full** content; the engine produces a ~500-char highlighted snippet (`highlighted_content`) marking query-matching tokens (`<mark>`), falling back to the doc's own top TF-IDF tokens. `get_all_documents`/`get_document_by_id` still truncate to 500 chars.
- The migration system is custom (not Alembic). New migrations go in `backend/migrations/` as numbered `.sql` files.
- PDF/DOCX extraction needs `pypdf`/`python-docx` (in `requirements.txt`); the loader returns a readable error if a library is missing.
