from typing import Literal

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from app.booking.database import save_booking
from app.booking.parser import parse_booking
from app.booking.router import detect_intent
from app.booking.service import booking_chat
from app.chunk_embed import (
    extract_text,
    fixed_chunk,
    generate_embeddings,
    recursive_chunk,
)
from app.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.database import Base, SessionLocal, engine
from app.models import Document
from app.rag.llm import generate_answer, rewrite_query
from app.rag.memory import (
    booking_active,
    end_booking,
    get_history,
    save_message,
    start_booking,
)
from app.rag.retriever import retrieve_chunks
from app.vector_store import store_embeddings

app = FastAPI(title="RAG Pipeline API")

# Create database tables
Base.metadata.create_all(bind=engine)


# ----------------------------
# Schemas
# ----------------------------

class ChatRequest(BaseModel):
    session_id:str
    question: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    context: list[str]


# ----------------------------
# Upload API
# ----------------------------

@app.post("/upload")
async def upload(file: UploadFile, strategy: Literal["fixed", "recursive"],):
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
        raise HTTPException(
            status_code=400,
            detail="Invalid strategy. Use 'fixed' or 'recursive'.",
        )

    embeddings = generate_embeddings(chunks)

    store_embeddings(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename,
    )

    db = SessionLocal()

    try:
        db.add(
            Document(
                filename=file.filename,
                chunk_strategy=strategy,
                num_chunks=len(chunks),
            )
        )
        db.commit()

    finally:
        db.close()

    return {
        "message": "Document uploaded successfully.",
        "filename": file.filename,
        "chunk_strategy": strategy,
        "chunks_created": len(chunks),
    }


# ----------------------------
# Chat API
# ----------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        # --------------------------------------------------
        # Load conversation history
        # --------------------------------------------------
        history = get_history(request.session_id)
        history_text = "\n".join(history)

        # --------------------------------------------------
        # Detect intent
        # --------------------------------------------------
        if booking_active(request.session_id):
            intent = "booking"

        else:
            intent = detect_intent(message=request.question)

            if intent == "booking":
                start_booking(request.session_id)

        # ==================================================
        # BOOKING FLOW
        # ==================================================
        if intent == "booking":

            # Save user message
            save_message(
                request.session_id,
                "user",
                request.question,
            )

            # Generate booking response
            reply = booking_chat(
                history=history_text,
                message=request.question,
            )

            booking = parse_booking(reply)

            # Booking completed
            if booking:

                save_booking(booking)

                end_booking(request.session_id)

                confirmation = "✅ Interview booked successfully."

                save_message(
                    request.session_id,
                    "assistant",
                    confirmation,
                )

                return ChatResponse(
                    question=request.question,
                    answer=confirmation,
                    context=[],
                )

            # Booking still in progress
            save_message(
                request.session_id,
                "assistant",
                reply,
            )

            return ChatResponse(
                question=request.question,
                answer=reply,
                context=[],
            )

        # ==================================================
        # RAG FLOW
        # ==================================================

        # Save user message
        save_message(
            request.session_id,
            "user",
            request.question,
        )

        query = rewrite_query(
            question=request.question,
            history=history_text,
        )

        chunks = retrieve_chunks(query)

        if not chunks:
            answer = "No relevant information found."

            save_message(
                request.session_id,
                "assistant",
                answer,
            )

            return ChatResponse(
                question=request.question,
                answer=answer,
                context=[],
            )

        context = "\n\n".join(
            f"[{i+1}] {chunk}"
            for i, chunk in enumerate(chunks)
        )

        answer = generate_answer(
            question=request.question,
            context=context,
            history=history_text,
        )

        save_message(
            request.session_id,
            "assistant",
            answer,
        )

        return ChatResponse(
            question=request.question,
            answer=answer,
            context=chunks,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {e}",
        )