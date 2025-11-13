from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.class_feature import ClassFeature
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClassModel


class ClassFeatureModel(Base):
    __tablename__ = "class_feature"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    level: Mapped[int]
    character_class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))

    character_class: Mapped[CharacterClassModel] = relationship(
        back_populates="features"
    )

    def to_domain(self) -> ClassFeature:
        return ClassFeature(
            feature_id=self.id,
            class_id=self.character_class_id,
            name=self.name,
            description=self.description,
            level=self.level,
            name_in_english=self.name_in_english,
        )

    @staticmethod
    def from_domain(feature: ClassFeature) -> ClassFeatureModel:
        return ClassFeatureModel(
            id=feature.feature_id(),
            name=feature.name(),
            description=feature.description(),
            name_in_english=feature.name_in_english(),
            level=feature.level(),
            character_class_id=feature.class_id(),
        )
