import streamlit as st
import os

from src.rag import build_vector_db, ask_question

st.set_page_config(
    page_title="Finance Education Assistant",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Personal Finance Education Assistant")
st.write("Learn financial concepts with AI using trusted educational documents.")

st.info(
    "This chatbot provides financial education only. "
    "It is not a financial advisor."
)

# Sidebar
with st.sidebar:
    st.header("Knowledge Base")

    st.write("Add educational PDF files to:")
    st.code("data/documents/")

    if st.button("📚 Index Financial Documents"):
        with st.spinner("Reading and processing documents..."):
            result = build_vector_db()
            st.success(result)

    st.divider()
    st.caption("Powered by Python, LangChain, ChromaDB and an LLM.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            with st.expander("📄 View Sources"):
                for source in message["sources"]:
                    st.write("•", source)

# Suggested questions
if not st.session_state.messages:
    st.subheader("Try asking")

    st.markdown("""
    - What is budgeting?
    - What is an emergency fund?
    - Explain inflation in simple words.
    - What is compound interest?
    - What is the difference between saving and investing?
    """)

# User input
question = st.chat_input("Ask a financial education question...")

if question:
    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching financial documents..."):
            try:
                answer, sources = ask_question(question)

                st.markdown(answer)

                if sources:
                    with st.expander("📄 View Sources"):
                        for source in sources:
                            st.write("•", source)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as e:
                st.error(f"An error occurred: {e}")