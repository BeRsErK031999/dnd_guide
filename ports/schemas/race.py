from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.race import Race, RaceAge, RaceFeature, RaceIncreaseModifier, RaceSpeed
from litestar.dto import DataclassDTO
from ports.schemas.length import LengthSchema


@dataclass
class RaceFeatureSchema:
    name: str
    description: str

    @staticmethod
    def from_domain(feature: RaceFeature) -> RaceFeatureSchema:
        return RaceFeatureSchema(
            name=feature.name(),
            description=feature.description(),
        )


@dataclass
class RaceAgeSchema:
    max_age: int
    description: str

    @staticmethod
    def from_domain(age: RaceAge) -> RaceAgeSchema:
        return RaceAgeSchema(
            max_age=age.max_age(),
            description=age.description(),
        )


@dataclass
class RaceSpeedSchema:
    base_speed: LengthSchema
    description: str

    @staticmethod
    def from_domain(speed: RaceSpeed) -> RaceSpeedSchema:
        return RaceSpeedSchema(
            base_speed=LengthSchema.from_domain(speed.base_speed()),
            description=speed.description(),
        )


@dataclass
class RaceIncreaseModifierSchema:
    modifier: str
    bonus: int

    @staticmethod
    def from_domain(modifier: RaceIncreaseModifier) -> RaceIncreaseModifierSchema:
        return RaceIncreaseModifierSchema(
            modifier=modifier.modifier(),
            bonus=modifier.bonus(),
        )


@dataclass
class ReadRaceSchema:
    race_id: UUID
    name: str
    description: str
    type_id: UUID
    size_id: UUID
    speed: RaceSpeedSchema
    age: RaceAgeSchema
    increase_modifiers: Sequence[RaceIncreaseModifierSchema]
    source_id: UUID
    features: Sequence[RaceFeatureSchema]
    name_in_english: str

    @staticmethod
    def from_domain(race: Race) -> ReadRaceSchema:
        return ReadRaceSchema(
            race_id=race.race_id(),
            name=race.name(),
            description=race.description(),
            type_id=race.type_id(),
            size_id=race.size_id(),
            speed=RaceSpeedSchema.from_domain(race.speed()),
            age=RaceAgeSchema.from_domain(race.age()),
            increase_modifiers=[
                RaceIncreaseModifierSchema.from_domain(modifier)
                for modifier in race.increase_modifiers()
            ],
            source_id=race.source_id(),
            features=[
                RaceFeatureSchema.from_domain(feature) for feature in race.features()
            ],
            name_in_english=race.name_in_english(),
        )


@dataclass
class CreateRaceSchema:
    name: str
    description: str
    type_id: UUID
    size_id: UUID
    speed: RaceSpeedSchema
    age: RaceAgeSchema
    increase_modifiers: Sequence[RaceIncreaseModifierSchema]
    source_id: UUID
    features: Sequence[RaceFeatureSchema]
    name_in_english: str


class CreateRaceDTO(DataclassDTO[CreateRaceSchema]):
    pass


@dataclass
class UpdateRaceSchema:
    name: str | None = None
    description: str | None = None
    type_id: UUID | None = None
    size_id: UUID | None = None
    speed: RaceSpeedSchema | None = None
    age: RaceAgeSchema | None = None
    increase_modifiers: Sequence[RaceIncreaseModifierSchema] | None = None
    new_features: Sequence[RaceFeatureSchema] | None = None
    add_features: Sequence[RaceFeatureSchema] | None = None
    remove_features: Sequence[str] | None = None
    name_in_english: str | None = None
    source_id: UUID | None = None


class UpdateRaceDTO(DataclassDTO[UpdateRaceSchema]):
    pass
