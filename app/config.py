import os

from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5" # vector = 384

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "documents"
VECTOR_SIZE = 384

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL= "llama-3.3-70b-versatile"
TOP_K = 3

REDIS_HOST = "localhost"
REDIS_PORT = 6379