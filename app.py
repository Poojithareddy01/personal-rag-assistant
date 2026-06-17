import streamlit as st
from ingest import ingest_pdf, ingest_url
from rag import get_answer
import tempfile, os

st.title("🧠 Personal RAG Assistant")

# Initialize chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
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

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared!")

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Chat input ---
question = st.chat_input("Ask a question about your documents...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_answer(question, st.session_state.messages)
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
