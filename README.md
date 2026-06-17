# 🧠 Personal RAG Assistant

A personal RAG (Retrieval-Augmented Generation) assistant that answers questions from your PDFs and URLs. Runs 100% locally — no API key needed.

## Stack
- **LangChain** — orchestration
- **ChromaDB** — local vector database
- **Ollama** (llama3.2:1b + nomic-embed-text) — free local LLM + embeddings
- **Streamlit** — web UI

## Setup

```bash
# 1. Install Ollama from ollama.com and pull models
ollama pull llama3.2:1b
ollama pull nomic-embed-text

# 2. Clone the repo
git clone https://github.com/Poojithareddy01/personal-rag-assistant.git
cd personal-rag-assistant

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install streamlit langchain langchain-community langchain-ollama \
            chromadb pypdf beautifulsoup4 requests python-dotenv langchain-text-splitters

# 5. Run
streamlit run app.py
```

## Usage
- Upload a PDF or paste a URL in the sidebar
- Ask questions in the main area
- Get answers from your own documents!
