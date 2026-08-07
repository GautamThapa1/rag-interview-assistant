from redis import Redis

from app.config import REDIS_HOST, REDIS_PORT

client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0, 
    decode_responses=True
    )

def save_message(session_id: str, role: str, message: str):
    client.rpush(
        session_id,
        f"{role}: {message}"
    )


def get_history(session_id: str) -> list[str]:
    return client.lrange(session_id, 0, -1) # get from 0 to last


def start_booking(session_id: str):
    client.set(f"booking:{session_id}", "active")


def booking_active(session_id: str) -> bool:
    return client.exists(f"booking:{session_id}") == 1


def end_booking(session_id: str):
    client.delete(f"booking:{session_id}")