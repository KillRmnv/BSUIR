-- Migration 008: Remove content column from documents table.
-- Content is now stored in S3 (MinIO) and fetched via s3_key.
-- This reduces DB size and leverages object storage for large texts.

ALTER TABLE documents DROP COLUMN IF EXISTS content;
