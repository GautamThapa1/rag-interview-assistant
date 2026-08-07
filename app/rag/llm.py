from groq import Groq

from app.config import LLM_MODEL

client = Groq()

SYSTEM_PROMPT = """
You are a helpful AI assistant for question answering.

Use ONLY the retrieved context to answer the user's question.

Rules:
- Do not use outside knowledge.
- If the answer is not in the context, reply:
  "I couldn't find that information in the uploaded documents."
- Do not make up facts.
- Keep your answers clear and concise.
- If multiple context sections are relevant, combine them into one answer.
"""


def generate_answer(
    question: str,
    context: str,
    history: str,
) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""Conversation History:
{history}

Retrieved Context:
{context}

Question:
{question}

Answer using only the retrieved context.""",
            },
        ],
    )

    return response.choices[0].message.content


def rewrite_query(question: str, history: str) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
Rewrite the user's latest question into a standalone question.

Use the conversation history only to resolve references like:
- it
- that
- explain more
- previous answer

Return ONLY the rewritten question.
If no rewrite is needed, return the original question.
""",
            },
            {
                "role": "user",
                "content": f"""
Conversation History:
{history}

Latest Question:
{question}
""",
            },
        ],
    )

    return response.choices[0].message.content.strip()