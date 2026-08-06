from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    chunk_strategy: Mapped[str]
    num_chunks: Mapped[int]
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )