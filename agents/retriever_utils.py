# agents/retriever_utils.py

import os
from typing import List
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# === Configuration ===
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_documents(directory: str) -> List[Document]:
    """
    Load all .txt files in the specified directory as LangChain Documents.
    """
    docs = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(directory, filename))
            docs.extend(loader.load())
    return docs


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into manageable chunks using a recursive splitter.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_documents(documents)


def create_or_load_vectorstore(doc_dir: str, db_dir: str) -> FAISS:
    """
    Create or load a FAISS vectorstore from treaty documents.
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    if os.path.exists(db_dir):
        print("🔁 Loading existing FAISS index...")
        return FAISS.load_local(db_dir, embeddings)

    print("📄 Loading documents and building FAISS index...")
    docs = load_documents(doc_dir)
    chunks = split_documents(docs)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(db_dir)
    print("✅ FAISS index saved to:", db_dir)
    return vectorstore
