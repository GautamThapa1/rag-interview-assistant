from groq import Groq

from app.config import LLM_MODEL

client = Groq()

SYSTEM_PROMPT = """
You are an intent classifier.

You are given the conversation history and the latest user message.

Return ONLY one word:

- rag
- booking

If the conversation is already about booking an interview,
continue returning booking even if the latest message is only:

- Hero
- Gautam
- tomorrow
- 3 PM
- my email is ...
"""


def detect_intent(message: str,) -> str:
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

Latest User Message:
{message}
""",
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip().lower()