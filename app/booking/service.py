from groq import Groq

from app.config import LLM_MODEL

client = Groq()

SYSTEM_PROMPT = """
You are an interview booking assistant.

Your goal is to collect:

- name
- email
- interview date
- interview time

Rules:
- Ask ONLY for the missing information.
- Do not ask again for information already provided.
- Be polite and conversational.
- When all required information has been collected, reply EXACTLY in this format:

BOOKING_COMPLETE
Name: <name>
Email: <email>
Date: <date>
Time: <time>
"""


def booking_chat(history: str, message: str) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
Conversation History:
{history}

User:
{message}
""",
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content