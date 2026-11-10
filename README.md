# rag_cli

A small command-line RAG (retrieval-augmented generation) project for learning AI engineering. It reads a document, splits it into chunks, turns each chunk into a vector embedding, and stores the vectors in PostgreSQL with pgvector so they can be searched by meaning.

## What you'll learn
- **Embeddings:** turning text into vectors that capture meaning
- **Text chunking:** splitting documents into searchable pieces
- **Semantic search:** finding chunks by similarity, not keywords
- **Supporting skills:** data ingestion, cosine similarity, basic prompt engineering, and database schema design

## How it works

```
PDF / Markdown ──► extract text ──► chunk ──► embed ──► PostgreSQL + pgvector
                                                              │
                         question ──► embed ──► similarity search ──► top chunks
```

| File | Purpose |
| --- | --- |
| `database.py` | Connects to Postgres and creates the `document_chunks` table |
| `ingest.py` | Extracts PDF text, chunks it, embeds it with `all-MiniLM-L6-v2`, and saves it |
| `chat.py` | Query side: semantic search (in progress) |

## Requirements
- Python 3.9+
- PostgreSQL with the [pgvector](https://github.com/pgvector/pgvector) extension

## Setup

1. **Install PostgreSQL and pgvector** (macOS with Homebrew):
   ```bash
   brew install postgresql@17 pgvector
   brew services start postgresql@17
   ```

2. **Create the database and enable pgvector:**
   ```bash
   createdb rag_cli
   psql rag_cli -c "CREATE EXTENSION IF NOT EXISTS vector;"
   ```

3. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Add a `.env` file** in the project root:
   ```
   DATABASE_URL=postgresql://<user>@localhost:5432/rag_cli
   ```

5. **Create the table:**
   ```bash
   python database.py
   ```

## Usage

Put a PDF at `data/test_document.pdf`, then run:

```bash
python ingest.py
```

The first run downloads the embedding model (about 90 MB). Each chunk is stored with a 384-dimension vector.

To check what was stored:

```bash
psql rag_cli -c "SELECT id, left(text_content, 80) FROM document_chunks LIMIT 5;"
```

## Roadmap
- [x] PDF text extraction
- [x] Fixed-size chunking
- [x] Local embeddings with SentenceTransformers
- [x] Storage in pgvector
- [ ] Markdown input
- [ ] Semantic chunking with overlap
- [ ] Source metadata (file, page, chunk index)
- [ ] Cosine-similarity search in `chat.py`
- [ ] Vector index (HNSW) for faster search
- [ ] Send retrieved chunks to an LLM to answer questions

## Notes
- `.env`, `data/`, and `*.pdf` are gitignored, so documents and secrets stay local.
- If you switch embedding models, update `vector(384)` in `database.py` to match the new model's output size.
