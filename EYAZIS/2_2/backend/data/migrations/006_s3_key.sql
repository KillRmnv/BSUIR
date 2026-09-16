-- Migration 006: Add s3_key column for MinIO object storage
ALTER TABLE documents ADD COLUMN IF NOT EXISTS s3_key VARCHAR(500);
