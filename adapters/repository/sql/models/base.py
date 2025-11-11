from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.now(timezone.utc),
    )
