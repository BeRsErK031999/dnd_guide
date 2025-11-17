from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.command.length import LengthCommand
from domain.error import DomainError


@dataclass
class RaceFeatureCommand:
    name: str
    description: str


@dataclass
class RaceAgeCommand:
    max_age: int
    description: str


@dataclass
class RaceSpeedCommand:
    base_speed: LengthCommand
    description: str


@dataclass
class RaceIncreaseModifierCommand:
    modifier: str
    bonus: int


@dataclass
class CreateRaceCommand:
    user_id: UUID
    name: str
    description: str
    creature_type: str
    creature_size: str
    speed: RaceSpeedCommand
    age: RaceAgeCommand
    increase_modifiers: Sequence[RaceIncreaseModifierCommand]
    source_id: UUID
    features: Sequence[RaceFeatureCommand]
    name_in_english: str


@dataclass
class UpdateRaceCommand:
    user_id: UUID
    race_id: UUID
    name: str | None = None
    description: str | None = None
    creature_size: str | None = None
    creature_type: str | None = None
    speed: RaceSpeedCommand | None = None
    age: RaceAgeCommand | None = None
    increase_modifiers: Sequence[RaceIncreaseModifierCommand] | None = None
    new_features: Sequence[RaceFeatureCommand] | None = None
    add_features: Sequence[RaceFeatureCommand] | None = None
    remove_features: Sequence[str] | None = None
    name_in_english: str | None = None
    source_id: UUID | None = None

    def __post_init__(self) -> None:
        if all(
            [
                self.name is None,
                self.description is None,
                self.creature_type is None,
                self.creature_size is None,
                self.speed is None,
                self.age is None,
                self.increase_modifiers is None,
                self.new_features is None,
                self.add_features is None,
                self.remove_features is None,
                self.name_in_english is None,
                self.source_id is None,
            ]
        ):
            raise DomainError.invalid_data("не переданы данные для обновления расы")
        if self.new_features is not None and (
            self.add_features is not None or self.remove_features is not None
        ):
            raise DomainError.invalid_data(
                "для умений расы нельзя одновременно назначить новый список и "
                "корректировать существующий"
            )
        if self.add_features is not None and self.remove_features is not None:
            for feature in self.add_features:
                if feature.name in self.remove_features:
                    raise DomainError.invalid_data(
                        f"умение с названием {feature.name} есть в списке для "
                        "удаления и для добавления"
                    )


@dataclass
class DeleteRaceCommand:
    user_id: UUID
    race_id: UUID
