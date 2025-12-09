from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.creature_size import CreatureSize
from domain.creature_type import CreatureType
from domain.modifier import Modifier
from domain.race import Race, RaceAge, RaceFeature, RaceIncreaseModifier, RaceSpeed

from .length import AppLength

__all__ = [
    "AppRace",
    "AppRaceFeature",
    "AppRaceAge",
    "AppRaceSpeed",
    "AppRaceIncreaseModifier",
]


@dataclass
class AppRaceFeature:
    name: str
    description: str

    @staticmethod
    def from_domain(feature: RaceFeature) -> "AppRaceFeature":
        return AppRaceFeature(
            name=feature.name(),
            description=feature.description(),
        )

    def to_domain(self) -> RaceFeature:
        return RaceFeature(
            name=self.name,
            description=self.description,
        )


@dataclass
class AppRaceAge:
    max_age: int
    description: str

    @staticmethod
    def from_domain(age: RaceAge) -> "AppRaceAge":
        return AppRaceAge(
            max_age=age.max_age(),
            description=age.description(),
        )

    def to_domain(self) -> RaceAge:
        return RaceAge(
            max_age=self.max_age,
            description=self.description,
        )


@dataclass
class AppRaceSpeed:
    base_speed: AppLength
    description: str

    @staticmethod
    def from_domain(speed: RaceSpeed) -> "AppRaceSpeed":
        return AppRaceSpeed(
            base_speed=AppLength.from_domain(speed.base_speed()),
            description=speed.description(),
        )

    def to_domain(self) -> RaceSpeed:
        return RaceSpeed(
            base_speed=self.base_speed.to_domain(),
            description=self.description,
        )


@dataclass
class AppRaceIncreaseModifier:
    modifier: str
    bonus: int

    @staticmethod
    def from_domain(modifier: RaceIncreaseModifier) -> "AppRaceIncreaseModifier":
        return AppRaceIncreaseModifier(
            modifier=modifier.modifier(),
            bonus=modifier.bonus(),
        )

    def to_domain(self) -> RaceIncreaseModifier:
        return RaceIncreaseModifier(
            modifier=Modifier.from_str(self.modifier),
            bonus=self.bonus,
        )


@dataclass
class AppRace:
    race_id: UUID
    name: str
    description: str
    creature_type: str
    creature_size: str
    speed: AppRaceSpeed
    age: AppRaceAge
    increase_modifiers: Sequence[AppRaceIncreaseModifier]
    source_id: UUID
    features: Sequence[AppRaceFeature]
    name_in_english: str

    @staticmethod
    def from_domain(race: Race) -> "AppRace":
        return AppRace(
            race_id=race.race_id(),
            name=race.name(),
            description=race.description(),
            creature_type=race.creature_type().value,
            creature_size=race.creature_size().value,
            speed=AppRaceSpeed.from_domain(race.speed()),
            age=AppRaceAge.from_domain(race.age()),
            increase_modifiers=[
                AppRaceIncreaseModifier.from_domain(modifier)
                for modifier in race.increase_modifiers()
            ],
            source_id=race.source_id(),
            features=[
                AppRaceFeature.from_domain(feature) for feature in race.features()
            ],
            name_in_english=race.name_in_english(),
        )

    def to_domain(self) -> Race:
        return Race(
            race_id=self.race_id,
            name=self.name,
            description=self.description,
            creature_type=CreatureType.from_str(self.creature_type),
            creature_size=CreatureSize.from_str(self.creature_size),
            speed=self.speed.to_domain(),
            age=self.age.to_domain(),
            increase_modifiers=[m.to_domain() for m in self.increase_modifiers],
            features=[f.to_domain() for f in self.features],
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )
