from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClassModel
    from adapters.repository.sql.models.spell import SpellModel
    from adapters.repository.sql.models.subclass_feature import SubclassFeatureModel


class CharacterSubclassModel(Base):
    __tablename__ = "character_subclass"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    character_class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped[CharacterClassModel] = relationship(
        back_populates="character_subclasses"
    )
    features: Mapped[SubclassFeatureModel] = relationship(
        back_populates="character_subclass"
    )
    spells: Mapped[list[SpellModel]] = relationship(
        back_populates="character_subclass", secondary="character_subclass_spell"
    )
