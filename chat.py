from sentence_transformers import SentenceTransformer
from database import get_connection, EMBEDDING_MODEL

# 1. Load the SAME model used during ingestion.
#    A different model would place text on a different "meaning map",
#    so its vectors couldn't be compared with the stored ones.
print("Loading embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL)

def search(conn, query, top_k=5):
    # 2. Turn the question into a vector.
    #    Keep it as a numpy array: pgvector maps numpy arrays to the
    #    `vector` type, while a plain Python list would be sent as float[]
    #    and the <=> operator wouldn't accept it.
    query_embedding = model.encode(query)

    # 3. Ask Postgres for the nearest chunks.
    #    <=> is pgvector's cosine DISTANCE operator:
    #      0 = same direction (same meaning), 1 = unrelated, 2 = opposite.
    #    Sorting by distance ascending gives the closest matches first.
    return conn.execute(
        """
        SELECT id, text_content, embedding <=> %(q)s AS distance
        FROM document_chunks
        ORDER BY distance
        LIMIT %(k)s
        """,
        {"q": query_embedding, "k": top_k},
    ).fetchall()

def print_results(results):
    if not results:
        print("No chunks in the database. Run ingest.py first.")
        return
    for rank, (chunk_id, text, distance) in enumerate(results, start=1):
        # Similarity is just the flip side of distance: higher = more similar
        similarity = 1 - distance
        snippet = " ".join(text.split())[:200]  # collapse newlines, shorten
        print(f"\n#{rank}  similarity={similarity:.3f}  (chunk id {chunk_id})")
        print(f"    {snippet}...")

if __name__ == "__main__":
    conn = get_connection()
    print("Ask a question about your document (type 'quit' to exit).")
    try:
        while True:
            query = input("\n> ").strip()
            if query.lower() in ("quit", "exit"):
                break
            if query:
                print_results(search(conn, query))
    except (KeyboardInterrupt, EOFError):
        print()  # Ctrl+C / Ctrl+D also exit cleanly
    finally:
        conn.close()
