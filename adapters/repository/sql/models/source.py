from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClassModel
    from adapters.repository.sql.models.race import RaceModel
    from adapters.repository.sql.models.spell import SpellModel


class SourceModel(Base):
    __tablename__ = "source"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(100))
    races: Mapped[list[RaceModel]] = relationship(back_populates="source")
    character_classes: Mapped[list[CharacterClassModel]] = relationship(
        back_populates="source"
    )
    spells: Mapped[list[SpellModel]] = relationship(back_populates="source")
