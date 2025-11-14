from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.character_subclass import CharacterSubclass
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

    def to_domain(self) -> CharacterSubclass:
        return CharacterSubclass(
            subclass_id=self.id,
            class_id=self.character_class_id,
            name=self.name,
            description=self.description,
            name_in_english=self.name_in_english,
        )

    @staticmethod
    def from_domain(character_subclass: CharacterSubclass) -> CharacterSubclassModel:
        return CharacterSubclassModel(
            id=character_subclass.subclass_id(),
            character_class_id=character_subclass.class_id(),
            name=character_subclass.name(),
            description=character_subclass.description(),
            name_in_english=character_subclass.name_in_english(),
        )
