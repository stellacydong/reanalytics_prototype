import os
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from mistral_langchain_wrapper import MistralLLM


# -------------------------
# CONFIG
# -------------------------
DATA_DIR = Path("data/treaty_samples/")
VECTOR_DB_PATH = Path("outputs/faiss_index")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# -------------------------
# Load / Ingest Docs
# -------------------------
def load_documents(directory: Path):
    documents = []
    for file in directory.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            documents.append(Document(page_content=text, metadata={"source": file.name}))
    return documents


# -------------------------
# Build Vector Index
# -------------------------
def build_or_load_vectorstore():
    if VECTOR_DB_PATH.exists():
        print("🔁 Loading existing FAISS index...")
        return FAISS.load_local(str(VECTOR_DB_PATH), HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME))

    print("📚 Ingesting and indexing treaty documents...")
    docs = load_documents(DATA_DIR)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(str(VECTOR_DB_PATH))
    return vectorstore


# -------------------------
# Query Function
# -------------------------
def query_treaty(question: str) -> str:
    print("🔍 Running RAG query...")
    vectorstore = build_or_load_vectorstore()
    retriever = vectorstore.as_retriever()

    # Inject your LLM wrapper
    llm = MistralLLM()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=False
    )

    return qa_chain.run(question)


# -------------------------
# CLI Test
# -------------------------
if __name__ == "__main__":
    query = "What coverage limits are mentioned in the treaty?"
    answer = query_treaty(query)
    print("\n💬 RAG Answer:\n", answer)

