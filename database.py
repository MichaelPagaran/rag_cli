import os
import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

# The embedding model and its output size live together on purpose:
# if you change the model, the vector(N) column below must change too.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

def get_connection():
    # Connect to the database
    conn = psycopg.connect(DB_URL, autocommit=True)
    
    # Register the vector type with psycopg so Python understands it
    register_vector(conn)
    return conn

def init_db():
    conn = get_connection()
    
    # Create a table for our document chunks
    # The vector size must match the embedding model's output (EMBEDDING_DIM)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            text_content TEXT NOT NULL,
            embedding vector({EMBEDDING_DIM})
        );
    """)
    print("Database table 'document_chunks' initialized successfully!")
    conn.close()

if __name__ == "__main__":
    init_db()