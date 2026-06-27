import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma
import chromadb

load_dotenv()

# Vercel Serverless Fix: Force FastEmbed to cache models in the writable /tmp directory
os.environ["FASTEMBED_CACHE_PATH"] = "/tmp/fastembed_cache"


# ── Document Loading ─────────────────────────────────────────
def load_pdf_files(data_path: str):
    """Load all PDF files from a directory."""
    loader = DirectoryLoader(
        data_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader,
    )
    documents = loader.load()
    return documents


# ── Text Splitting ───────────────────────────────────────────
def text_split(documents, chunk_size=500, chunk_overlap=50):
    """Split documents into smaller chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_documents(documents)
    return chunks


# ── Embeddings ───────────────────────────────────────────────
def get_embeddings():
    """Load embeddings via FastEmbed (ONNX-based, no scipy/sentence-transformers needed)."""
    return FastEmbedEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    )


# ── ChromaDB Cloud Connection ───────────────────────────────
def get_chroma_client():
    """Create a ChromaDB Cloud client from .env credentials."""
    return chromadb.CloudClient(
        api_key=os.environ["CHROMA_API_KEY"],
        tenant=os.environ["CHROMA_TENANT"],
        database=os.environ["CHROMA_DATABASE"],
    )


def get_vector_store(embedding=None):
    """Connect to the existing ChromaDB Cloud vector store."""
    if embedding is None:
        embedding = get_embeddings()

    client = get_chroma_client()
    collection_name = os.environ.get("CHROMA_COLLECTION", "medical_chatbot")

    vector_store = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embedding,
    )
    return vector_store


def create_vector_store(documents, embedding=None):
    """Create a new vector store from documents and upload to ChromaDB Cloud in batches."""
    if embedding is None:
        embedding = get_embeddings()

    client = get_chroma_client()
    collection_name = os.environ.get("CHROMA_COLLECTION", "medical_chatbot")

    vector_store = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embedding,
    )

    batch_size = 250
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        vector_store.add_documents(batch)
        print(f"      Uploaded batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")

    return vector_store
