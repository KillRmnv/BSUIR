-- Migration 004: Add language column to documents

-- 1. Language column — 'en' or 'fr', populated at upload time
ALTER TABLE documents ADD COLUMN IF NOT EXISTS lang VARCHAR(10);

-- 2. Backfill existing rows (all seed corpus docs are English)
UPDATE documents SET lang = 'en' WHERE lang IS NULL;

-- Record this migration
INSERT INTO schema_migrations (migration_name) VALUES ('004_add_lang') ON CONFLICT DO NOTHING;
