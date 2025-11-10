from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column


class Timestamp:
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.now(timezone.utc),
    )
