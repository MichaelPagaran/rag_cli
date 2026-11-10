# rag_cli

A learning project: the first in a series of AI engineering projects. The point is to understand each piece, not just to ship working code.

## Learning goals
- Master embeddings
- Text chunking
- Basic semantic search

## Key skills to practice
- Data ingestion
- Vector math (cosine similarity)
- Basic prompt engineering
- Database schema design

## Workflow
1. Parse a complex PDF or Markdown file.
2. Split the text into manageable semantic chunks.
3. Convert the chunks to vector embeddings, using either an API (like OpenAI) or a local model (via SentenceTransformers).
4. Store the embeddings in a local PostgreSQL database with the pgvector extension.
5. Run semantic search over the stored chunks (and later feed the results into an LLM prompt).

## Current state
- `database.py`: connection (`DATABASE_URL` from `.env`) and `init_db()`, which creates `document_chunks (id, text_content, embedding vector(384))`.
- `ingest.py`: PDF extraction with `pypdf`, fixed 500-character chunking, embeddings with `all-MiniLM-L6-v2` (384 dimensions), one insert per chunk. Reads `data/test_document.pdf`.
- `chat.py`: empty. Will hold the query/search side.
- Not yet covered: Markdown input, semantic (non-fixed-size) chunking, chunk overlap, source metadata (file, page, chunk index), a vector index, and cosine-similarity search.

## Conventions
- Python, with dependencies in `requirements.txt` and a local `.venv`.
- Secrets live in `.env` (gitignored). Never print or commit them.
- `data/` and `*.pdf` are gitignored. Don't commit test documents.
- If the embedding model changes, the `vector(N)` dimension in `database.py` must match the model's output size.

## How to help
- Explain the *why* behind each change (for example, why a chunk size or overlap was chosen, or what cosine distance means in pgvector), concisely and with analogies for harder concepts.
- Prefer small, incremental steps the user can follow and run, over large rewrites.
- Match the existing style: short, commented, beginner-readable scripts.
