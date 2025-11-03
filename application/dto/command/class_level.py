from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.error import DomainError


@dataclass
class ClassLevelDiceCommand:
    dice: str
    description: str
    number: int = 1


@dataclass
class ClassLevelPointsCommand:
    points: int
    description: str


@dataclass
class ClassLevelBonusDamageCommand:
    damage: int
    description: str


@dataclass
class ClassLevelIncreaseSpeedCommand:
    speed: int
    unit: str
    description: str


@dataclass
class CreateClassLevelCommand:
    user_id: UUID
    class_id: UUID
    level: int
    dice: ClassLevelDiceCommand | None
    spell_slots: Sequence[int] | None
    number_cantrips_know: int | None
    number_spells_know: int | None
    number_arcanums_know: int | None
    points: ClassLevelPointsCommand | None
    bonus_damage: ClassLevelBonusDamageCommand | None
    increase_speed: ClassLevelIncreaseSpeedCommand | None


@dataclass
class UpdateClassLevelCommand:
    user_id: UUID
    class_level_id: UUID
    class_id: UUID | None
    level: int | None
    dice: ClassLevelDiceCommand | None
    spell_slots: Sequence[int] | None
    number_cantrips_know: int | None
    number_spells_know: int | None
    number_arcanums_know: int | None
    points: ClassLevelPointsCommand | None
    bonus_damage: ClassLevelBonusDamageCommand | None
    increase_speed: ClassLevelIncreaseSpeedCommand | None

    def __post_init__(self) -> None:
        if all(
            [
                self.class_id is None,
                self.level is None,
                self.dice is None,
                self.spell_slots is None,
                self.number_cantrips_know is None,
                self.number_spells_know is None,
                self.number_arcanums_know is None,
                self.points is None,
                self.bonus_damage is None,
                self.increase_speed is None,
            ]
        ):
            raise DomainError.invalid_data(
                "не передано данных для обновления уровня класса"
            )


@dataclass
class DeleteClassLevelCommand:
    user_id: UUID
    class_level_id: UUID
