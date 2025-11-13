from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.subclass_feature import SubclassFeature
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_subclass import CharacterSubclassModel


class SubclassFeatureModel(Base):
    __tablename__ = "subclass_feature"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    level: Mapped[int]
    character_subclass_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_subclass.id")
    )

    character_subclass: Mapped[CharacterSubclassModel] = relationship(
        back_populates="features"
    )

    def to_domain(self) -> SubclassFeature:
        return SubclassFeature(
            feature_id=self.id,
            subclass_id=self.character_subclass_id,
            name=self.name,
            description=self.description,
            level=self.level,
            name_in_english=self.name_in_english,
        )

    @staticmethod
    def from_domain(feature: SubclassFeature) -> SubclassFeatureModel:
        return SubclassFeatureModel(
            id=feature.feature_id(),
            name=feature.name(),
            description=feature.description(),
            name_in_english=feature.name_in_english(),
            level=feature.level(),
            character_subclass_id=feature.subclass_id(),
        )
