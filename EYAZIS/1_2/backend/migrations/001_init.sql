-- Migration 001: Create pgvector extension and base tables
-- This migration runs FIRST to ensure pgvector is available

-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Documents table with vector embeddings
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    embedding vector(1000)
);

-- 3. Search logs table for analytics
CREATE TABLE IF NOT EXISTS search_logs (
    id SERIAL PRIMARY KEY,
    query_text TEXT,
    query_embedding vector(1000),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Migration tracking table
CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    migration_name VARCHAR(255) NOT NULL UNIQUE,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Record this migration
INSERT INTO schema_migrations (migration_name) VALUES ('001_init') ON CONFLICT DO NOTHING;
