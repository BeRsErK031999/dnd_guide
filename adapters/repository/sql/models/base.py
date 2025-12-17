from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        # server_default=text("TIMEZONE('utc', now())")
        default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        # server_default=text("TIMEZONE('utc', now())"),
        default=utcnow,
        onupdate=utcnow,
    )
