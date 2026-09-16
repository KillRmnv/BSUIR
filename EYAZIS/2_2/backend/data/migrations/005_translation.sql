-- Таблица словаря перевода (EN → FR)
CREATE TABLE IF NOT EXISTS translation_dictionary (
    id SERIAL PRIMARY KEY,
    source_word VARCHAR(255) NOT NULL,
    target_word VARCHAR(255) NOT NULL,
    source_pos VARCHAR(20) NOT NULL DEFAULT '',
    target_pos VARCHAR(20) NOT NULL DEFAULT '',
    frequency INTEGER NOT NULL DEFAULT 1,
    UNIQUE(source_word, target_word, source_pos)
);

CREATE INDEX IF NOT EXISTS idx_dict_source ON translation_dictionary(source_word);
CREATE INDEX IF NOT EXISTS idx_dict_target ON translation_dictionary(target_word);
CREATE INDEX IF NOT EXISTS idx_dict_source_pos ON translation_dictionary(source_word, source_pos);
