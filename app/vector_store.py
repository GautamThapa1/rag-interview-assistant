import hashlib

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import COLLECTION_NAME, QDRANT_URL, VECTOR_SIZE

client = QdrantClient(url=QDRANT_URL)


def create_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.DOT),
        )

def store_embeddings(chunks, embeddings, filename):
    create_collection()

    points = []
    for chunk, embedding in zip(chunks, embeddings):
        point_id = hashlib.sha256(f"{filename}:{chunk}".encode("utf-8")).hexdigest()
        points.append(
            PointStruct(id=point_id, vector=embedding, payload={"text": chunk, "filename": filename},)
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )