# Personal Finance Education Assistant Using RAG

An AI-powered financial education chatbot that answers beginner-friendly
questions using trusted financial educational documents.

## Problem

Financial information is often complex and difficult for beginners to understand.
This project helps users learn basic financial concepts through an AI chatbot.

## Features

- Answers financial literacy questions
- Uses PDF educational documents as its knowledge base
- Retrieves relevant document passages
- Generates answers using an LLM
- Displays source document names
- Provides beginner-friendly explanations

## Technologies

- Python
- Streamlit
- LangChain
- ChromaDB
- Sentence Transformers
- Groq LLM API

## Architecture

PDF Documents → Text Extraction → Chunking → Embeddings
→ ChromaDB → Retrieval → LLM → Answer with Sources

## Topics

- Budgeting
- Saving
- Emergency funds
- Inflation
- Interest
- Banking
- Financial terminology

## Disclaimer

This application is for financial education only.
It does not provide personalized financial advice.

## Run Locally

1. Clone the repository.
2. Install dependencies.
3. Configure the Groq API key in `.env`.
4. Add PDF documents inside `data/documents/`.
5. Index the documents in the application.
6. Run the application.

## Author

Student project – AI in Finance.