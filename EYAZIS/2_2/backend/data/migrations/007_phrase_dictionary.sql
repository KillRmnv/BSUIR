-- Таблица фразового словаря (multi-word expressions)
CREATE TABLE IF NOT EXISTS phrase_dictionary (
    id SERIAL PRIMARY KEY,
    source_phrase VARCHAR(500) NOT NULL,
    target_phrase VARCHAR(500) NOT NULL,
    frequency INTEGER NOT NULL DEFAULT 1,
    UNIQUE(source_phrase)
);

CREATE INDEX IF NOT EXISTS idx_phrase_source ON phrase_dictionary(source_phrase);
