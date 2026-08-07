# Conversational RAG API

A custom Retrieval-Augmented Generation (RAG) API built with FastAPI. The application supports document question answering, conversational memory, and an LLM-powered interview booking workflow.

**Repository:** :contentReference[oaicite:0]{index=0}

---

## Features

- Upload PDF documents
- Fixed and Recursive chunking
- SentenceTransformer embeddings
- Qdrant vector database
- Custom RAG pipeline (without LangChain RetrievalQA)
- Conversational memory using Redis
- Query rewriting for follow-up questions
- LLM-powered interview booking
- SQLite metadata and booking storage
- FastAPI REST API

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Qdrant
- Redis
- Groq API
- SentenceTransformers
- Docker

---

## Project Structure

```text
app/
├── booking/
│   ├── database.py
│   ├── models.py
│   ├── parser.py
│   ├── router.py
│   └── service.py
├── rag/
│   ├── llm.py
│   ├── memory.py
│   └── retriever.py
├── chunk_embed.py
├── config.py
├── database.py
├── main.py
├── models.py
└── vector_store.py
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/GautamThapa1/palmmind_task.git
cd palmmind_task
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Copy `.env.example` to `.env`

```bash
cp .env.example .env
```

Update the following variable:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Start Qdrant

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -v qdrant_data:/qdrant/storage \
  qdrant/qdrant
```

---

## Start Redis

```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis
```

---

## Run the API

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Upload Document

```
POST /upload
```

Uploads a PDF, extracts text, chunks it, generates embeddings, stores vectors in Qdrant, and saves document metadata to SQLite.

---

### Chat

```
POST /chat
```

Supports:

- Conversational RAG
- Multi-turn conversations
- Query rewriting
- Interview booking

---

## Architecture

### Document Ingestion

```text
PDF
 │
 ▼
Text Extraction
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
Qdrant
```

### Question Answering

```text
User Question
      │
      ▼
Query Rewriting
      │
      ▼
Retriever (Qdrant)
      │
      ▼
Groq LLM
      │
      ▼
Answer
```

### Interview Booking

```text
User
 │
 ▼
Intent Detection
 │
 ├───────────── RAG
 │
 └───────────── Booking
                   │
                   ▼
        Collect user information
                   │
                   ▼
          Store booking in SQLite
```

---

## Storage

| Component | Purpose |
|----------|---------|
| SQLite | Document metadata & interview bookings |
| Qdrant | Vector embeddings |
| Redis | Conversation memory & booking state |


