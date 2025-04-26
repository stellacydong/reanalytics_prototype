# agents/treaty_rag_agent.py

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from models.mistral_model_loader import load_mistral_model


class TreatyRAGAgent:
    """
    Treaty Retrieval-Augmented Generation (RAG) Agent for answering reinsurance treaty questions.
    """

    def __init__(self, model_pipeline=None, vectorstore_path="faiss_index"):
        """
        Initialize the RAG agent.

        Args:
        - model_pipeline: Optional external LLM pipeline. If None, will load Mistral locally.
        - vectorstore_path: Local path to store FAISS index.
        """
        self.vectorstore_path = vectorstore_path

        # Load the LLM pipeline
        if model_pipeline is None:
            self.llm = HuggingFacePipeline(pipeline=load_mistral_model())
        else:
            self.llm = model_pipeline

        # Initialize variables
        self.vectorstore = None
        self.qa_chain = None

    def ingest_treaty(self, treaty_file_path):
        """
        Load and ingest the treaty file for question answering.
        """
        loader = TextLoader(treaty_file_path)
        documents = loader.load()

        # Split documents
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.split_documents(documents)

        # Create embeddings
        embeddings = HuggingFaceEmbeddings()

        # Build or load vectorstore
        if os.path.exists(self.vectorstore_path):
            self.vectorstore = FAISS.load_local(self.vectorstore_path, embeddings)
        else:
            self.vectorstore = FAISS.from_documents(docs, embeddings)
            self.vectorstore.save_local(self.vectorstore_path)

        # Create RetrievalQA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True
        )

    def ask(self, query):
        """
        Ask a question based on the ingested treaty.

        Args:
        - query: The user question string.

        Returns:
        - answer: The LLM-generated answer based on retrieved treaty chunks.
        """
        if self.qa_chain is None:
            raise ValueError("Treaty not ingested yet. Please upload and ingest a treaty first.")

        result = self.qa_chain({"query": query})
        answer = result["result"]
        return answer

# Example direct usage
if __name__ == "__main__":
    agent = TreatyRAGAgent()
    agent.ingest_treaty("data/sample_treaty.txt")
    response = agent.ask("What is the retention amount?")
    print("Answer:", response)

