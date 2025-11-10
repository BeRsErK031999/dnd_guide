from adapters.repository.sql.models.base import Base
from adapters.repository.sql.models.mixin import Timestamp
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Source(Timestamp, Base):
    __tablename__ = "source"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(100))
