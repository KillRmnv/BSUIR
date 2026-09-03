-- Migration 003: Auto-summary + file watcher support

-- 1. Auto-summary column (generated at indexing time)
ALTER TABLE documents ADD COLUMN IF NOT EXISTS summary TEXT;

-- 2. File path column — binds a document to a file on disk so the
--    watcher can upsert (re-index) or delete the exact document
ALTER TABLE documents ADD COLUMN IF NOT EXISTS file_path VARCHAR(1000);
CREATE UNIQUE INDEX IF NOT EXISTS idx_documents_file_path
    ON documents(file_path) WHERE file_path IS NOT NULL;

-- 3. Watch clients — machines monitoring local directories
CREATE TABLE IF NOT EXISTS watch_clients (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL UNIQUE,
    watched_dir VARCHAR(1000) NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Watch events log
CREATE TABLE IF NOT EXISTS watch_events (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    old_path VARCHAR(1000) DEFAULT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Record this migration
INSERT INTO schema_migrations (migration_name) VALUES ('003_file_watchers') ON CONFLICT DO NOTHING;