from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from adapters.repository.sql.models.mixin import Timestamp
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClass
    from adapters.repository.sql.models.spell import Spell
    from adapters.repository.sql.models.subclass_feature import SubclassFeature


class CharacterSubclass(Timestamp, Base):
    __tablename__ = "character_subclass"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    character_class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClass"] = relationship(
        back_populates="character_subclasses"
    )
    features: Mapped["SubclassFeature"] = relationship(
        back_populates="character_subclass"
    )
    spells: Mapped[list["Spell"]] = relationship(
        back_populates="character_subclass", secondary="character_subclass_spell"
    )
