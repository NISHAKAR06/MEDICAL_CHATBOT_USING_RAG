"""
store_index.py — One-time script to ingest PDFs into ChromaDB Cloud.

Usage:
    python store_index.py
"""
from src.helper import load_pdf_files, text_split, get_embeddings, create_vector_store


def main():
    print("=" * 60)
    print("  Medical Chatbot — Document Ingestion")
    print("=" * 60)

    # 1. Load PDFs
    print("\n[1/4] Loading PDF files from data/ ...")
    documents = load_pdf_files("data")
    print(f"      Loaded {len(documents)} pages")

    # 2. Split into chunks
    print("\n[2/4] Splitting into text chunks ...")
    chunks = text_split(documents)
    print(f"      Created {len(chunks)} chunks")

    # 3. Load embedding model
    print("\n[3/4] Loading embedding model ...")
    embedding = get_embeddings()
    print("      Model loaded: sentence-transformers/all-MiniLM-L6-v2")

    # 4. Upload to ChromaDB Cloud
    print("\n[4/4] Uploading to ChromaDB Cloud ...")
    vector_store = create_vector_store(chunks, embedding)
    count = vector_store._collection.count()
    print(f"      Stored {count} documents in ChromaDB Cloud")

    print("\n" + "=" * 60)
    print("  [OK] Ingestion complete! You can now run: python app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
