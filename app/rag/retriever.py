from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from app.config import COLLECTION_NAME, EMBEDDING_MODEL, QDRANT_URL, TOP_K

model = SentenceTransformer(EMBEDDING_MODEL)
client = QdrantClient(url=QDRANT_URL)


def retrieve_chunks(question: str):
    embed_query = model.encode(
        question,
        normalize_embeddings=True,
    ).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embed_query,
        limit=TOP_K * 3,
    ).points

    unique_texts = []
    seen_texts = set()
    for point in results:
        text = point.payload.get("text")
        if not text or text in seen_texts:
            continue
        seen_texts.add(text)
        unique_texts.append(text)
        if len(unique_texts) >= TOP_K:
            break

    return unique_texts
