import streamlit as st
from ingest import ingest_pdf, ingest_url
from rag import get_answer
import tempfile, os

st.title("🧠 Personal RAG Assistant")

# --- Sidebar: Ingest documents ---
with st.sidebar:
    st.header("📥 Add to Knowledge Base")
    
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file and st.button("Ingest PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(uploaded_file.read())
            tmp_path = f.name
        ingest_pdf(tmp_path)
        os.unlink(tmp_path)
        st.success("✅ PDF added!")
    
    url = st.text_input("Or paste a URL")
    if url and st.button("Ingest URL"):
        ingest_url(url)
        st.success("✅ URL added!")

# --- Main: Ask questions ---
st.header("💬 Ask a Question")
question = st.text_input("What do you want to know?")

if question:
    with st.spinner("Thinking... (may take 10-15 seconds)"):
        answer = get_answer(question)
    st.write(answer)