from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from models.mistral_langchain_wrapper import MistralLLM

import os

# Constants
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DATA_DIR = "data/treaty_samples"
INDEX_PATH = "outputs/faiss_index"

# Step 1: Load documents
def load_documents():
    docs = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_DIR, filename)
            loader = TextLoader(path)
            docs.extend(loader.load())
    return docs

# Step 2: Split & Embed
def build_vectorstore():
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectordb = FAISS.from_documents(chunks, embedder)
    vectordb.save_local(INDEX_PATH)
    return vectordb

# Step 3: Load RAG chain
def load_rag_chain():
    vectordb = FAISS.load_local(INDEX_PATH, HuggingFaceEmbeddings(model_name=EMBED_MODEL))
    retriever = vectordb.as_retriever()
    llm = MistralLLM()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain

# Step 4: Inference API
def answer_treaty_question(query: str) -> str:
    chain = load_rag_chain()
    result = chain(query)
    return result["result"]
