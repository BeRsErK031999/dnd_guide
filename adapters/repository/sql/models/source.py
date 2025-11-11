from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClass
    from adapters.repository.sql.models.race import Race
    from adapters.repository.sql.models.spell import Spell


class Source(Base):
    __tablename__ = "source"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(100))
    races: Mapped[list["Race"]] = relationship(back_populates="source")
    character_classes: Mapped[list["CharacterClass"]] = relationship(
        back_populates="source"
    )
    spells: Mapped[list["Spell"]] = relationship(back_populates="source")
