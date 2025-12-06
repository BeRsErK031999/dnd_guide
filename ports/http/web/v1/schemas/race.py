from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.model.race import (
    AppRace,
    AppRaceAge,
    AppRaceFeature,
    AppRaceIncreaseModifier,
    AppRaceSpeed,
)
from ports.http.web.v1.schemas.length import LengthSchema


@dataclass
class RaceFeatureSchema:
    name: str
    description: str

    @staticmethod
    def from_app(feature: AppRaceFeature) -> "RaceFeatureSchema":
        return RaceFeatureSchema(name=feature.name, description=feature.description)


@dataclass
class RaceAgeSchema:
    max_age: int
    description: str

    @staticmethod
    def from_app(age: AppRaceAge) -> "RaceAgeSchema":
        return RaceAgeSchema(max_age=age.max_age, description=age.description)


@dataclass
class RaceSpeedSchema:
    base_speed: LengthSchema
    description: str

    @staticmethod
    def from_app(speed: AppRaceSpeed) -> "RaceSpeedSchema":
        return RaceSpeedSchema(
            base_speed=LengthSchema.from_app(speed.base_speed),
            description=speed.description,
        )


@dataclass
class RaceIncreaseModifierSchema:
    modifier: str
    bonus: int

    @staticmethod
    def from_app(modifier: AppRaceIncreaseModifier) -> "RaceIncreaseModifierSchema":
        return RaceIncreaseModifierSchema(
            modifier=modifier.modifier, bonus=modifier.bonus
        )


@dataclass
class ReadRaceSchema:
    race_id: UUID
    name: str
    description: str
    creature_type: str
    creature_size: str
    speed: RaceSpeedSchema
    age: RaceAgeSchema
    increase_modifiers: Sequence[RaceIncreaseModifierSchema]
    source_id: UUID
    features: Sequence[RaceFeatureSchema]
    name_in_english: str

    @staticmethod
    def from_app(race: AppRace) -> "ReadRaceSchema":
        return ReadRaceSchema(
            race_id=race.race_id,
            name=race.name,
            description=race.description,
            creature_type=race.creature_type,
            creature_size=race.creature_size,
            speed=RaceSpeedSchema.from_app(race.speed),
            age=RaceAgeSchema.from_app(race.age),
            increase_modifiers=[
                RaceIncreaseModifierSchema.from_app(m) for m in race.increase_modifiers
            ],
            source_id=race.source_id,
            features=[RaceFeatureSchema.from_app(f) for f in race.features],
            name_in_english=race.name_in_english,
        )


@dataclass
class CreateRaceSchema:
    name: str
    description: str
    creature_type: str
    creature_size: str
    speed: RaceSpeedSchema
    age: RaceAgeSchema
    increase_modifiers: Sequence[RaceIncreaseModifierSchema]
    source_id: UUID
    features: Sequence[RaceFeatureSchema]
    name_in_english: str


@dataclass
class UpdateRaceSchema:
    name: str | None = None
    description: str | None = None
    creature_type: str | None = None
    creature_size: str | None = None
    speed: RaceSpeedSchema | None = None
    age: RaceAgeSchema | None = None
    increase_modifiers: Sequence[RaceIncreaseModifierSchema] | None = None
    new_features: Sequence[RaceFeatureSchema] | None = None
    add_features: Sequence[RaceFeatureSchema] | None = None
    remove_features: Sequence[str] | None = None
    name_in_english: str | None = None
    source_id: UUID | None = None
