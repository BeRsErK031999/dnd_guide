from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column


class Name:
    name: Mapped[str] = mapped_column(unique=True)

    __table_args__ = CheckConstraint(
        "LENGTH(name) > 0 AND LENGTH(name) < 50", name="check_name_length"
    )


class Description:
    description: Mapped[str] = mapped_column(default="")


class Timestamp:
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.now(timezone.utc),
    )
