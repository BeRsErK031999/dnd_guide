from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.length import AppLength
from application.dto.model.race import (
    AppRace,
    AppRaceAge,
    AppRaceFeature,
    AppRaceIncreaseModifier,
    AppRaceSpeed,
)
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.source import SourceModel
    from adapters.repository.sql.models.subrace import SubraceModel


class RaceModel(Base):
    __tablename__ = "race"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    base_speed: Mapped[float]
    speed_description: Mapped[str]
    max_age: Mapped[int]
    age_description: Mapped[str]
    creature_type: Mapped[str] = mapped_column(String(50))
    creature_size: Mapped[str] = mapped_column(String(50))
    source_id: Mapped[UUID] = mapped_column(ForeignKey("source.id"))

    increase_modifiers: Mapped[list["RaceIncreaseModifierModel"]] = relationship(
        back_populates="race", cascade="all, delete-orphan"
    )
    features: Mapped[list["RaceFeatureModel"]] = relationship(
        back_populates="race", cascade="all, delete-orphan"
    )
    source: Mapped["SourceModel"] = relationship(back_populates="races")
    subraces: Mapped[list["SubraceModel"]] = relationship(back_populates="race")

    def to_app(self) -> AppRace:
        return AppRace(
            race_id=self.id,
            name=self.name,
            description=self.description,
            creature_type=self.creature_type,
            creature_size=self.creature_size,
            speed=AppRaceSpeed(AppLength(self.base_speed), self.speed_description),
            age=AppRaceAge(self.max_age, self.age_description),
            increase_modifiers=[im.to_app() for im in self.increase_modifiers],
            features=[f.to_app() for f in self.features],
            source_id=self.source_id,
            name_in_english=self.name_in_english,
        )

    @staticmethod
    def from_app(race: AppRace) -> "RaceModel":
        return RaceModel(
            id=race.race_id,
            name=race.name,
            description=race.description,
            name_in_english=race.name_in_english,
            base_speed=race.speed.base_speed.count,
            speed_description=race.speed.description,
            max_age=race.age.max_age,
            age_description=race.age.description,
            creature_type=race.creature_type,
            creature_size=race.creature_size,
            source_id=race.source_id,
        )


class RaceIncreaseModifierModel(Base):
    __tablename__ = "race_increase_modifier"

    name: Mapped[str] = mapped_column(String(50))
    bonus: Mapped[int]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id", ondelete="CASCADE"))

    race: Mapped["RaceModel"] = relationship(back_populates="increase_modifiers")

    def to_app(self) -> AppRaceIncreaseModifier:
        return AppRaceIncreaseModifier(
            modifier=self.name,
            bonus=self.bonus,
        )

    @staticmethod
    def from_app(
        race_id: UUID, modifier: AppRaceIncreaseModifier
    ) -> "RaceIncreaseModifierModel":
        return RaceIncreaseModifierModel(
            name=modifier.modifier,
            bonus=modifier.bonus,
            race_id=race_id,
        )


class RaceFeatureModel(Base):
    __tablename__ = "race_feature"

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id", ondelete="CASCADE"))

    race: Mapped["RaceModel"] = relationship(back_populates="features")

    def to_app(self) -> AppRaceFeature:
        return AppRaceFeature(
            name=self.name,
            description=self.description,
        )

    @staticmethod
    def from_app(race_id: UUID, feature: AppRaceFeature) -> "RaceFeatureModel":
        return RaceFeatureModel(
            name=feature.name,
            description=feature.description,
            race_id=race_id,
        )
