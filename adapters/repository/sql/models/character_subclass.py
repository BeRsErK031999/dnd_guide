from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.character_subclass import AppSubclass
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

    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="character_subclasses"
    )
    features: Mapped["SubclassFeatureModel"] = relationship(
        back_populates="character_subclass", cascade="all, delete-orphan"
    )
    spells: Mapped[list["SpellModel"]] = relationship(
        back_populates="character_subclasses", secondary="rel_spell_character_subclass"
    )

    def to_app(self) -> AppSubclass:
        return AppSubclass(
            subclass_id=self.id,
            class_id=self.character_class_id,
            name=self.name,
            description=self.description,
            name_in_english=self.name_in_english,
        )

    @staticmethod
    def from_app(subclass: AppSubclass) -> "CharacterSubclassModel":
        return CharacterSubclassModel(
            id=subclass.subclass_id,
            character_class_id=subclass.class_id,
            name=subclass.name,
            description=subclass.description,
            name_in_english=subclass.name_in_english,
        )
