from sqlalchemy import Column, Integer, String

from app.database import Base


class InterviewBooking(Base):
    __tablename__ = "interview_bookings"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    date = Column(String, nullable=False)
    time = Column(String, nullable=False)