from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

CHROMA_DIR = "./chroma_db"

def get_answer(question: str, chat_history: list) -> str:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatOllama(model="llama3.2:1b", temperature=0)

    # Build history text from last 10 exchanges
    history_text = ""
    for msg in chat_history[-10:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    prompt = PromptTemplate.from_template("""
You are a helpful assistant. Use the context and chat history to answer the question.
If you don't know, say you don't know.

Chat History:
{chat_history}

Context from documents:
{context}

Question: {question}

Answer:
""")

    # Retrieve relevant chunks
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "chat_history": history_text,
        "context": context,
        "question": question
    })

    return answer
