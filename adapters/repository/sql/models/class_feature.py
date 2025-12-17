from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.class_feature import AppClassFeature
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
    character_class_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_class.id", ondelete="CASCADE")
    )

    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="features"
    )

    def to_app(self) -> AppClassFeature:
        return AppClassFeature(
            feature_id=self.id,
            class_id=self.character_class_id,
            name=self.name,
            description=self.description,
            level=self.level,
            name_in_english=self.name_in_english,
        )

    @staticmethod
    def from_app(feature: AppClassFeature) -> "ClassFeatureModel":
        return ClassFeatureModel(
            id=feature.feature_id,
            character_class_id=feature.class_id,
            name=feature.name,
            description=feature.description,
            level=feature.level,
            name_in_english=feature.name_in_english,
        )
