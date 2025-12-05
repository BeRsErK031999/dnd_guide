from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.subrace import (
    AppSubrace,
    AppSubraceFeature,
    AppSubraceIncreaseModifier,
)
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.race import RaceModel


class SubraceModel(Base):
    __tablename__ = "subrace"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))

    race: Mapped["RaceModel"] = relationship(back_populates="subraces")
    increase_modifiers: Mapped[list["SubraceIncreaseModifierModel"]] = relationship(
        back_populates="subrace"
    )
    features: Mapped[list["SubraceFeatureModel"]] = relationship(
        back_populates="subrace"
    )

    def to_app(self) -> AppSubrace:
        return AppSubrace(
            subrace_id=self.id,
            race_id=self.race_id,
            name=self.name,
            description=self.description,
            increase_modifiers=[im.to_app() for im in self.increase_modifiers],
            features=[f.to_app() for f in self.features],
            name_in_english=self.name_in_english,
        )

    @staticmethod
    def from_domain(subrace: AppSubrace) -> "SubraceModel":
        return SubraceModel(
            id=subrace.subrace_id,
            name=subrace.name,
            description=subrace.description,
            name_in_english=subrace.name_in_english,
            race_id=subrace.race_id,
        )


class SubraceIncreaseModifierModel(Base):
    __tablename__ = "subrace_increase_modifier"

    name: Mapped[str] = mapped_column(String(50))
    bonus: Mapped[int]
    subrace_id: Mapped[UUID] = mapped_column(ForeignKey("subrace.id"))

    subrace: Mapped["SubraceModel"] = relationship(back_populates="increase_modifiers")

    def to_app(self) -> AppSubraceIncreaseModifier:
        return AppSubraceIncreaseModifier(modifier=self.name, bonus=self.bonus)

    @staticmethod
    def from_app(
        modifier: AppSubraceIncreaseModifier,
    ) -> "SubraceIncreaseModifierModel":
        return SubraceIncreaseModifierModel(
            name=modifier.modifier, bonus=modifier.bonus
        )


class SubraceFeatureModel(Base):
    __tablename__ = "subrace_feature"

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str]
    subrace_id: Mapped[UUID] = mapped_column(ForeignKey("subrace.id"))

    subrace: Mapped["SubraceModel"] = relationship(back_populates="features")

    def to_app(self) -> AppSubraceFeature:
        return AppSubraceFeature(name=self.name, description=self.description)

    @staticmethod
    def from_app(feature: AppSubraceFeature) -> "SubraceFeatureModel":
        return SubraceFeatureModel(name=feature.name, description=feature.description)
