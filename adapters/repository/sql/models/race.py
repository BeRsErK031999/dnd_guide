from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.length import Length, LengthUnit
from domain.modifier import Modifier
from domain.race import Race, RaceAge, RaceFeature, RaceIncreaseModifier, RaceSpeed
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.creature_size import CreatureSizeModel
    from adapters.repository.sql.models.creature_type import CreatureTypeModel
    from adapters.repository.sql.models.source import SourceModel


class RaceModel(Base):
    __tablename__ = "race"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    base_speed: Mapped[float]
    speed_description: Mapped[str]
    max_age: Mapped[int]
    age_description: Mapped[str]
    creature_type_id: Mapped[UUID] = mapped_column(ForeignKey("creature_type.id"))
    creature_size_id: Mapped[UUID] = mapped_column(ForeignKey("creature_size.id"))
    source_id: Mapped[UUID] = mapped_column(ForeignKey("source.id"))

    creature_type: Mapped["CreatureTypeModel"] = relationship(back_populates="races")
    creature_size: Mapped["CreatureSizeModel"] = relationship(back_populates="races")
    increase_modifiers: Mapped[list[RaceIncreaseModifierModel]] = relationship(
        back_populates="race"
    )
    features: Mapped[list[RaceFeatureModel]] = relationship(back_populates="race")
    source: Mapped[SourceModel] = relationship(back_populates="races")

    def to_domain(self) -> Race:
        return Race(
            race_id=self.id,
            name=self.name,
            description=self.description,
            type_id=self.creature_type_id,
            size_id=self.creature_size_id,
            speed=RaceSpeed(
                Length(count=self.base_speed, unit=LengthUnit.FT),
                self.speed_description,
            ),
            age=RaceAge(self.max_age, self.age_description),
            increase_modifiers=[im.to_domain() for im in self.increase_modifiers],
            features=[f.to_domain() for f in self.features],
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )

    @staticmethod
    def from_domain(race: Race) -> RaceModel:
        return RaceModel(
            id=race.race_id(),
            name=race.name(),
            description=race.description(),
            name_in_english=race.name_in_english(),
            base_speed=race.speed().base_speed().in_ft(),
            speed_description=race.speed().description(),
            max_age=race.age().max_age(),
            age_description=race.age().description(),
            creature_type_id=race.type_id(),
            creature_size_id=race.size_id(),
            source_id=race.source_id(),
        )


class RaceIncreaseModifierModel(Base):
    __tablename__ = "race_increase_modifier"

    name: Mapped[str] = mapped_column(String(50))
    bonus: Mapped[int]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped[RaceModel] = relationship(back_populates="increase_modifiers")

    def to_domain(self) -> RaceIncreaseModifier:
        return RaceIncreaseModifier(
            modifier=Modifier.from_str(self.name),
            bonus=self.bonus,
        )

    @staticmethod
    def from_domain(
        race_id: UUID, increase_modifier: RaceIncreaseModifier
    ) -> RaceIncreaseModifierModel:
        return RaceIncreaseModifierModel(
            name=increase_modifier.modifier().name,
            bonus=increase_modifier.bonus(),
            race_id=race_id,
        )


class RaceFeatureModel(Base):
    __tablename__ = "race_feature"

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped[RaceModel] = relationship(back_populates="features")

    def to_domain(self) -> RaceFeature:
        return RaceFeature(
            name=self.name,
            description=self.description,
        )

    @staticmethod
    def from_domain(race_id: UUID, feature: RaceFeature) -> RaceFeatureModel:
        return RaceFeatureModel(
            name=feature.name(),
            description=feature.description(),
            race_id=race_id,
        )
