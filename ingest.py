from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

CHROMA_DIR = "./chroma_db"

def ingest_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    _store_documents(docs)
    print(f"✅ Ingested PDF: {pdf_path}")

def ingest_url(url: str):
    loader = WebBaseLoader(url)
    docs = loader.load()
    _store_documents(docs)
    print(f"✅ Ingested URL: {url}")

def _store_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)
