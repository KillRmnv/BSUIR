# README.md — EYAZIS/1_2 (IR System)

## What this is

Flask + PostgreSQL (pgvector) information retrieval system with TF-IDF vectorization. Vanilla JS frontend served by Flask. Dockerized. Includes a separate file watcher client for automatic document re-indexing.

## Quick start

```bash
docker-compose up --build
```

App at `http://localhost:5000`. Corpus is loaded automatically on first start from `backend/documents/*.txt`.

## Architecture

- `backend/app.py` — Flask entry point, serves API + static frontend
- `backend/document_processor.py` — TF-IDF vectorization, text cleaning, vocabulary building, token highlighting, extractive summary generation
- `backend/document_loader.py` — file upload strategy: extracts text from .txt/.md/.pdf/.docx/.html/.rtf/.csv/.log by extension
- `backend/search_engine.py` — Search orchestration (vectorize query → pgvector similarity search), builds highlighted snippets per result
- `backend/database_manager.py` — All PostgreSQL operations (CRUD, vector search via `<=>` operator)
- `backend/evaluator.py` — Search quality metrics (Precision, Recall, F-Score) + chart generation
- `backend/watch_handler.py` — Server-side processing of file watcher events (upsert/delete documents)
- `backend/migrate.py` — Custom migration runner (reads `backend/migrations/*.sql`, tracks in `schema_migrations` table)
- `backend/migrations/` — SQL migrations (001_init, 002_vocab_idf, 003_file_watchers)
- `backend/documents/` — Seed corpus (12 documents, ~7000 words total)
- `frontend/` — Static HTML/JS/CSS, no build step
- `file_watcher/` — Standalone CLI client for monitoring local directories

## Language identification (Variant 7: EN/FR, HTML)

Three methods, final answer by majority vote (`backend/lang_methods.py`):

- **N-gram** (Cavnar & Trenkle out-of-place, top-300 char 1–5 profiles): `backend/lang_ngram.py`, profiles `lang_profiles/ngram_{en,fr}.json`
- **Alphabet** (FR diacritics + marker words, tuned threshold): `backend/lang_alphabet.py`, params `lang_profiles/alphabet.json`
- **Neural** (LogisticRegression on char TF-IDF 1–5): `backend/lang_detect.py`, model `lang_profiles/ml_model.pkl` (gitignored, auto-retrains on startup)
- `backend/lang_text.py` — `<body>` extraction (drops script/style/markup) + FR-aware preprocessing (keeps `é è ç œ…`; separate from the search pipeline's `clean_text`, which is English-only)
- `backend/lang_seeds.py` + `backend/build_lang_corpus.py` — offline training corpora (`training/en.txt`, `training/fr.txt`, ~36 Kb each) + 10 test HTML docs (`test_html/*.html`, ~A4) + `manifest.csv` with ground truth
- `backend/train_lang_model.py` — offline CLI without Flask/DB: `train`, `classify <file>`, `batch` (accuracy + confusion + ms/doc for the report)
- `frontend/classify.html` (+ `js/classify.js`) — «Классификация» tab (Russian): model status/train, single file-or-text classify, batch over `test_html/` with accuracy/confusion/avg-ms table, CSV download + print
- `frontend/help.html` — fully static Russian help (no server calls): Variant 7 theory by category + search-glossary of the current functionality

```bash
cd backend
python build_lang_corpus.py        # regenerate corpora + test HTML (deterministic, seed=7)
python train_lang_model.py train   # neural needs scikit-learn (in Docker image); ngram+alphabet train anywhere
python train_lang_model.py batch   # per-method accuracy + confusion + ms/doc for the report
```

Measured offline (10 test HTML, ~A4 each): N-gram 10/10 @ ~8 ms/doc, alphabet 10/10 @ ~1 ms/doc (neural trains in Docker).

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/lang/status` | Is the model trained? (+ training metadata) |
| POST | `/api/lang/train` | Train all three methods from `training/*.txt` |
| POST | `/api/lang/classify` | Classify one doc (file upload or JSON `{text}`) → vote + per-method details + `agreed` |
| POST | `/api/lang/classify-batch` | Classify all `test_html/` → vote + per-method accuracy/confusion/avg-ms |

## File watcher

A separate CLI tool that monitors a local directory and pushes file change events (create/modify/delete) to the IR server for automatic re-indexing.

```bash
cd file_watcher
source venv/bin/activate
pip install -r requirements.txt
python watch_client.py /path/to/dir
```

### CLI options

| Flag | Description | Default |
|------|-------------|---------|
| `directory` | Directory to monitor (required) | — |
| `-s, --server` | IR server URL | `$IR_SERVER_URL` or `http://localhost:5000` |
| `-c, --client-id` | Unique client identifier | hostname |
| `-r, --recursive` | Watch subdirectories recursively | off |
| `-e, --ext` | Comma-separated file extensions | `.txt,.md,.pdf,.docx,.html,.rtf,.csv,.log` |
| `-d, --debounce` | Debounce interval in seconds | `2.0` |
| `-f, --state-file` | Path to state file | `<dir>/.watch_state.json` |
| `--no-register` | Skip client registration on startup | off |

### How it works

The client saves a `.watch_state.json` file in the watched directory containing `{filepath: {mtime, size}}` for every indexed file. On each startup it compares the current filesystem against the saved state and sends only the diff:

- **new files** → `created` events
- **changed files** (mtime or size differs) → `modified` events
- **deleted files** (in state but not on disk) → `deleted` events

During runtime, `watchdog` catches live changes and sends them immediately. The state file is updated after each successful server response.

```bash
cd file_watcher && source venv/bin/activate

# First run — scans all files, creates .watch_state.json
python watch_client.py ../test_documents

# Later — finds only new/changed/deleted files automatically
python watch_client.py ../test_documents

# Custom state file location
python watch_client.py ../test_documents -f /tmp/my_state.json
```

## Key constraints

- Vector dimension is **5000** — hardcoded in `app.py:30`, `search_engine.py:20`, `migrations/001_init.sql:13,20`, and `watch_handler.py:44`. All must match.
- NLTK data (`stopwords`, `punkt`) downloaded at Docker build time.
- DB credentials in `docker-compose.yml` (`ir_user` / `ir_password` / `ir_system`). App reads them via env vars with localhost defaults.
- Vocabulary and IDF are **in-memory globals** in `document_processor.py` (`VOCAB`, `IDF`). They are rebuilt on startup and after uploads automatically.
- Custom migration system in `backend/migrations/` (not Alembic). New migrations go as numbered `.sql` files.
- Auto-summary: `document_processor.generate_summary()` extracts top-3 sentences by TF-IDF at index time, stored in `documents.summary`.
- The `file_watcher/` venv is independent from `backend/` — separate dependencies, separate Python environment.

## API endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/init-db` | Run migrations + load `backend/documents/*.txt` |
| POST | `/api/search` | Vector search (`{query, top_k}`) |
| POST | `/api/upload` | Index a document (`{title, content}`) |
| POST | `/api/upload-file` | Upload a file (.txt/.md/.pdf/.docx/.html/.rtf/.csv/.log) |
| GET | `/api/documents` | List all documents |
| GET | `/api/documents/<id>` | Get document detail (with optional `?query=` highlighting) |
| DELETE | `/api/documents/<id>` | Delete a document |
| POST | `/api/metrics` | Evaluate search quality (precision/recall/F1) |
| GET | `/api/stats` | Document count |
| POST | `/api/watch-event` | Receive file watcher events from clients |
| GET/POST | `/api/watch-clients` | List or register watch clients |
| GET | `/api/help` | Theoretical terms and navigation guide |

## Gotchas

- No test suite, no linter, no formatter configured. Verify changes by running the app and testing manually.
- Flask serves frontend as static files (`static_folder="frontend"`). HTML pages reference JS via relative paths — no bundling.
- Search results: `search_documents` returns the **full** content; the engine produces a highlighted snippet (`highlighted_content`) marking query-matching tokens (`<mark>`).
- PDF/DOCX extraction needs `pypdf`/`python-docx` (in `requirements.txt`); the loader returns a readable error if a library is missing.
- To reset the database: `docker-compose down -v && docker-compose up --build`

## Report compilation (`EYAZIS_report/`)

### Prerequisites

```bash
# Arch Linux
sudo pacman -S texlive-most graphviz

# Ubuntu/Debian
sudo apt install texlive-full graphviz

# macOS
brew install --cask mactex-no-gui
brew install graphviz
```

### Compile report

```bash
cd EYAZIS_report

# Compile PDF (run twice for cross-references)
pdflatex -interaction=nonstopmode course_report.tex
pdflatex -interaction=nonstopmode course_report.tex

# Or with latexmk (auto-runs until stable)
latexmk -pdf course_report.tex

# Clean auxiliary files
latexmk -C
```

### Regenerate PlantUML diagrams

```bash
cd EYAZIS_report

# Using local plantuml.jar + graphviz
java -jar /path/to/plantuml.jar -tpng plantuml/*.puml -o png/

# Or with GRAPHVIZ_DOT env if dot is not in PATH
GRAPHVIZ_DOT=/path/to/dot java -jar /path/to/plantuml.jar -tpng plantuml/*.puml -o png/
```

Diagram source files are in `plantuml/*.puml`, output PNGs in `png/`. LaTeX auto-loads PNGs from `png/` via `\graphicspath`.
