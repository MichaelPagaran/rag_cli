-- Runs once, the first time the database volume is created.
-- pgvector is installed in the image, but each database must enable it.
CREATE EXTENSION IF NOT EXISTS vector;
