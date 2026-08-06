from fastapi import FastAPI, HTTPException, UploadFile

from app.chunk_embed import (
    extract_text,
    fixed_chunk,
    generate_embeddings,
    recursive_chunk,
)
from app.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.database import Base, SessionLocal, engine
from app.models import Document
from app.vector_store import store_embeddings

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/upload")
async def upload(file: UploadFile, strategy: str):
    text = extract_text(file)

    if strategy == "fixed":
        chunks = fixed_chunk(
            text,
            chunk_size=CHUNK_SIZE,
            overlap=CHUNK_OVERLAP,
        )
    elif strategy == "recursive":
        chunks = recursive_chunk(
            text,
            chunk_size=CHUNK_SIZE,
            overlap=CHUNK_OVERLAP,
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid strategy")

    embeddings = generate_embeddings(chunks)

    store_embeddings(
    chunks=chunks,
    embeddings=embeddings,
    filename=file.filename,
    )

    db = SessionLocal()

    db.add(
        Document(
            filename=file.filename,
            chunk_strategy=strategy,
            num_chunks=len(chunks),
        )
    )

    db.commit()
    db.close()

    return {
        "message": "Document uploaded successfully.",
        "filename": file.filename,
        "chunk_strategy": strategy,
        "chunks_created": len(chunks),
    }