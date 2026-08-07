from io import BytesIO

from fastapi import UploadFile
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")



def extract_text(file: UploadFile) -> str:

    # cuz txt file in just one file with no pages 
    if file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")

    elif file.filename.endswith(".pdf"):
        pdf = PdfReader(BytesIO(file.file.read()))

        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

        return text
    
    raise ValueError("Unsupported file type")


def fixed_chunk(text: str, chunk_size: int, overlap: int):
    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(text), step):
        chunks.append(text[i:i + chunk_size])

    return chunks


def recursive_chunk(text: str, chunk_size: int, overlap: int):
    paragraphs = text.split("\n\n")

    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) <= chunk_size:
            current += paragraph + "\n\n"
        else:
            if current:
                chunks.append(current.strip())

            # Start next chunk with overlap(-ve means from opposite) 
            # and new paragraph
            current = current[-overlap:] + paragraph + "\n\n"

    if current:
        chunks.append(current.strip())

    return chunks


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    return model.encode(chunks, normalize_embeddings=True).tolist()
