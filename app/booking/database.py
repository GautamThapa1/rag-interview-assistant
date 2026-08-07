from app.booking.models import InterviewBooking
from app.database import SessionLocal


def save_booking(data):
    db = SessionLocal()

    try:
        booking = InterviewBooking(
            name=data["name"],
            email=data["email"],
            date=data["date"],
            time=data["time"],
        )

        db.add(booking)
        db.commit()

    finally:
        db.close()