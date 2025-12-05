from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.class_level import (
    ClassLevel,
    ClassLevelBonusDamage,
    ClassLevelDice,
    ClassLevelIncreaseSpeed,
    ClassLevelPoints,
)
from domain.class_level.spell_slots import ClassLevelSpellSlots

from .dice import AppDice
from .length import AppLength


@dataclass
class AppClassLevelDice:
    dice: AppDice
    description: str

    @staticmethod
    def from_domain(level_dice: ClassLevelDice) -> "AppClassLevelDice":
        return AppClassLevelDice(
            dice=AppDice.from_domain(level_dice.dice()),
            description=level_dice.description(),
        )

    def to_domain(self) -> ClassLevelDice:
        return ClassLevelDice(
            dice=self.dice.to_domain(), dice_description=self.description
        )


@dataclass
class AppClassLevelPoints:
    points: int
    description: str

    @staticmethod
    def from_domain(level_points: ClassLevelPoints) -> "AppClassLevelPoints":
        return AppClassLevelPoints(
            points=level_points.points(),
            description=level_points.description(),
        )

    def to_domain(self) -> ClassLevelPoints:
        return ClassLevelPoints(points=self.points, description=self.description)


@dataclass
class AppClassLevelBonusDamage:
    damage: int
    description: str

    @staticmethod
    def from_domain(
        level_bonus_damage: ClassLevelBonusDamage,
    ) -> "AppClassLevelBonusDamage":
        return AppClassLevelBonusDamage(
            damage=level_bonus_damage.damage(),
            description=level_bonus_damage.description(),
        )

    def to_domain(self) -> ClassLevelBonusDamage:
        return ClassLevelBonusDamage(damage=self.damage, description=self.description)


@dataclass
class AppClassLevelIncreaseSpeed:
    speed: AppLength
    description: str

    @staticmethod
    def from_domain(
        level_increase_speed: ClassLevelIncreaseSpeed,
    ) -> "AppClassLevelIncreaseSpeed":
        return AppClassLevelIncreaseSpeed(
            speed=AppLength.from_domain(level_increase_speed.speed()),
            description=level_increase_speed.description(),
        )

    def to_domain(self) -> ClassLevelIncreaseSpeed:
        return ClassLevelIncreaseSpeed(
            speed=self.speed.to_domain(), description=self.description
        )


@dataclass
class AppClassLevel:
    class_level_id: UUID
    class_id: UUID
    level: int
    dice: AppClassLevelDice | None = None
    spell_slots: Sequence[int] | None = None
    number_cantrips_know: int | None = None
    number_spells_know: int | None = None
    number_arcanums_know: int | None = None
    points: AppClassLevelPoints | None = None
    bonus_damage: AppClassLevelBonusDamage | None = None
    increase_speed: AppClassLevelIncreaseSpeed | None = None

    @staticmethod
    def from_domain(level: ClassLevel) -> "AppClassLevel":
        dice = level.dice()
        slots = level.spell_slots()
        points = level.points()
        bonus_damage = level.bonus_damage()
        increase_speed = level.increase_speed()
        return AppClassLevel(
            class_level_id=level.level_id(),
            class_id=level.class_id(),
            level=level.level(),
            dice=AppClassLevelDice.from_domain(dice) if dice is not None else None,
            spell_slots=slots.slots() if slots is not None else None,
            number_cantrips_know=level.number_cantrips_know(),
            number_spells_know=level.number_spells_know(),
            number_arcanums_know=level.number_arcanums_know(),
            points=(
                AppClassLevelPoints.from_domain(points) if points is not None else None
            ),
            bonus_damage=(
                AppClassLevelBonusDamage.from_domain(bonus_damage)
                if bonus_damage is not None
                else None
            ),
            increase_speed=(
                AppClassLevelIncreaseSpeed.from_domain(increase_speed)
                if increase_speed is not None
                else None
            ),
        )

    def to_domain(self) -> ClassLevel:
        return ClassLevel(
            level_id=self.class_level_id,
            class_id=self.class_id,
            level=self.level,
            dice=self.dice.to_domain() if self.dice is not None else None,
            spell_slots=(
                ClassLevelSpellSlots(self.spell_slots)
                if self.spell_slots is not None
                else None
            ),
            number_cantrips_know=self.number_cantrips_know,
            number_spells_know=self.number_spells_know,
            number_arcanums_know=self.number_arcanums_know,
            points=self.points.to_domain() if self.points is not None else None,
            bonus_damage=(
                self.bonus_damage.to_domain() if self.bonus_damage is not None else None
            ),
            increase_speed=(
                self.increase_speed.to_domain()
                if self.increase_speed is not None
                else None
            ),
        )
