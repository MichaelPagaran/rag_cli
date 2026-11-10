import os
import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    # Connect to the database
    conn = psycopg.connect(DB_URL, autocommit=True)
    
    # Register the vector type with psycopg so Python understands it
    register_vector(conn)
    return conn

def init_db():
    conn = get_connection()
    
    # Create a table for our document chunks
    # We use vector(384) because our embedding model outputs 384 dimensions
    conn.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            text_content TEXT NOT NULL,
            embedding vector(384)
        );
    """)
    print("Database table 'document_chunks' initialized successfully!")
    conn.close()

if __name__ == "__main__":
    init_db()