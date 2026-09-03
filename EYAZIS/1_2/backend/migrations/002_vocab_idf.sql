-- Migration 002: Create vocabulary and IDF tables for persistence

-- 1. Vocabulary table — stores word → vector index mapping
CREATE TABLE IF NOT EXISTS vocabulary (
    id SERIAL PRIMARY KEY,
    word VARCHAR(255) NOT NULL UNIQUE,
    vector_index INTEGER NOT NULL
);

-- 2. IDF values table — stores word → IDF value
CREATE TABLE IF NOT EXISTS idf_values (
    id SERIAL PRIMARY KEY,
    word VARCHAR(255) NOT NULL UNIQUE,
    idf_value DOUBLE PRECISION NOT NULL
);

-- Record this migration
INSERT INTO schema_migrations (migration_name) VALUES ('002_vocab_idf') ON CONFLICT DO NOTHING;
