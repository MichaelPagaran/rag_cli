import os
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from database import get_connection, EMBEDDING_MODEL

# 1. Load the local embedding model (downloads automatically the first time)
print("Loading embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL)

def extract_text_from_pdf(pdf_path):
    print(f"Extracting text from {pdf_path}...")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text 

def chunk_text(text, chunk_size=500):
    # Basic chunking: split text into 500-character blocks
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def ingest_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    
    print(f"Created {len(chunks)} chunks. Generating embeddings and saving to database...")
    
    conn = get_connection()
    
    for chunk in chunks:
        if not chunk.strip():
            continue
            
        # 2. Turn the text chunk into a vector array
        embedding = model.encode(chunk).tolist()
        
        # 3. Insert the text and its vector into Postgres
        conn.execute(
            "INSERT INTO document_chunks (text_content, embedding) VALUES (%s, %s)",
            (chunk, embedding)
        )
        
    conn.close()
    print("Ingestion complete!")

if __name__ == "__main__":
    pdf_file = "data/test_document.pdf"
    
    if os.path.exists(pdf_file):
        ingest_pdf(pdf_file)
    else:
        print(f"Please place a PDF file at {pdf_file} and try again.")