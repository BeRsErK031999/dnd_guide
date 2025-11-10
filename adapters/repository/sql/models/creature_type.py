from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
from adapters.repository.sql.models.mixin import Timestamp
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.race import Race


class CreatureType(Timestamp, Base):
    __tablename__ = "creature_type"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    races: Mapped[list["Race"]] = relationship(back_populates="creature_type")
