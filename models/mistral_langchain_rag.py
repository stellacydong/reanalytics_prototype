import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from mistral_langchain_wrapper import MistralLLM

DATA_DIR = "data/treaty_samples"

# 1. Load treaty files
def load_treaties(path=DATA_DIR):
    docs = []
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(os.path.join(path, filename), "r") as file:
                content = file.read()
                docs.append(Document(page_content=content, metadata={"source": filename}))
    return docs

# 2. Embed and store
def create_faiss_retriever(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(split_docs, embedder)

# 3. Query treaty RAG
def query_treaty(query: str, retriever, llm):
    retrieved_docs = retriever.similarity_search(query, k=4)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    prompt = f"Given the treaty clauses below, answer the question:\n\n{context}\n\nQuestion: {query}"
    return llm.invoke(prompt)

if __name__ == "__main__":
    llm = MistralLLM()
    docs = load_treaties()
    retriever = create_faiss_retriever(docs)

    # Example query
    result = query_treaty("What is the retention level specified?", retriever, llm)
    print("\n🔍 RAG Result:\n", result)
