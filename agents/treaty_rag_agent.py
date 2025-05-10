# agents/treaty_rag_agent.py

import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# 1. Load treaty documents from data/treaty_samples/
def load_treaties(treaty_dir="data/treaty_samples/"):
    documents = []
    for filename in os.listdir(treaty_dir):
        if filename.endswith(".txt"):
            path = os.path.join(treaty_dir, filename)
            loader = TextLoader(path)
            documents.extend(loader.load())
    return documents

# 2. Split text into chunks
def chunk_documents(documents, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

# 3. Embed and build FAISS index
def create_faiss_index(chunks):
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embedding=embedder)
    return db

# 4. Load local Mistral model with HuggingFace Pipeline
def load_llm_pipeline():
    model_id = "mistralai/Mistral-7B-Instruct-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype=torch.float16)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm

# 5. Build RAG-style QA chain
def build_qa_chain(llm, vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain

if __name__ == "__main__":
    print("🔍 Loading and indexing treaty documents...")
    docs = load_treaties()
    chunks = chunk_documents(docs)
    vectordb = create_faiss_index(chunks)

    print("🚀 Loading Mistral LLM...")
    llm = load_llm_pipeline()

    print("🤖 Initializing QA chain...")
    qa = build_qa_chain(llm, vectordb)

    print("\n💬 Ask questions about the treaties. Type 'exit' to quit.\n")
    while True:
        query = input("🔹 Question: ")
        if query.lower() in ["exit", "quit"]:
            break
        result = qa(query)
        print(f"🧠 Answer:\n{result['result']}\n")

