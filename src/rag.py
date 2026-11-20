import os
import shutil

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

load_dotenv()

DOCUMENTS_PATH = "data/documents"
DB_PATH = "chroma_db"

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def build_vector_db():
    """Load PDFs, split text, and store embeddings."""

    loader = PyPDFDirectoryLoader(DOCUMENTS_PATH)
    documents = loader.load()

    if not documents:
        return "No PDF documents found."

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    # Remove old database to avoid duplicate chunks
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    return f"Successfully indexed {len(chunks)} text chunks."


def ask_question(question):
    """Retrieve relevant chunks and generate an answer."""

    if not os.path.exists(DB_PATH):
        return "Please index your financial documents first.", []

    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = f"""
You are a Personal Finance Education Assistant.

Answer the user's question using ONLY the context below.

Rules:
- Explain concepts in simple language.
- Do not invent facts.
- If the context does not contain the answer, say:
  "I could not find this information in my financial documents."
- Do not give personalized investment or financial advice.
- Provide educational information only.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    sources = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown document")
        page = doc.metadata.get("page", None)

        source_name = os.path.basename(source)

        if page is not None:
            source_name += f" (Page {page + 1})"

        if source_name not in sources:
            sources.append(source_name)

    return response.content, sources