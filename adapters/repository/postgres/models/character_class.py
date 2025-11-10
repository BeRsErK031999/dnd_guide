from adapters.repository.postgres.models.base import Base
from adapters.repository.postgres.models.mixin import Description, Name, Timestamp
from sqlalchemy.orm import Mapped, mapped_column


class CharacterClass(Name, Description, Timestamp, Base):
    name_in_english: Mapped[str] = mapped_column(default="")
