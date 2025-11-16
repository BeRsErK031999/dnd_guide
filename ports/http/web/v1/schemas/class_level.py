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
from ports.http.web.v1.schemas.dice import DiceSchema
from ports.http.web.v1.schemas.length import LengthSchema


@dataclass
class ClassLevelDiceSchema:
    dice: DiceSchema
    description: str

    @staticmethod
    def from_domain(level_dice: ClassLevelDice) -> ClassLevelDiceSchema:
        return ClassLevelDiceSchema(
            dice=DiceSchema.from_domain(level_dice.dice()),
            description=level_dice.description(),
        )


@dataclass
class ClassLevelPointsSchema:
    points: int
    description: str

    @staticmethod
    def from_domain(level_points: ClassLevelPoints) -> ClassLevelPointsSchema:
        return ClassLevelPointsSchema(
            points=level_points.points(),
            description=level_points.description(),
        )


@dataclass
class ClassLevelBonusDamageSchema:
    damage: int
    description: str

    @staticmethod
    def from_domain(
        level_bonus_damage: ClassLevelBonusDamage,
    ) -> ClassLevelBonusDamageSchema:
        return ClassLevelBonusDamageSchema(
            damage=level_bonus_damage.damage(),
            description=level_bonus_damage.description(),
        )


@dataclass
class ClassLevelIncreaseSpeedSchema:
    speed: LengthSchema
    description: str

    @staticmethod
    def from_domain(
        level_increase_speed: ClassLevelIncreaseSpeed,
    ) -> ClassLevelIncreaseSpeedSchema:
        return ClassLevelIncreaseSpeedSchema(
            speed=LengthSchema.from_domain(level_increase_speed.speed()),
            description=level_increase_speed.description(),
        )


@dataclass
class ReadClassLevelSchema:
    class_level_id: UUID
    class_id: UUID
    level: int
    dice: ClassLevelDiceSchema | None
    spell_slots: Sequence[int] | None
    number_cantrips_know: int | None
    number_spells_know: int | None
    number_arcanums_know: int | None
    points: ClassLevelPointsSchema | None
    bonus_damage: ClassLevelBonusDamageSchema | None
    increase_speed: ClassLevelIncreaseSpeedSchema | None

    @staticmethod
    def from_domain(level: ClassLevel) -> ReadClassLevelSchema:
        dice = level.dice()
        slots = level.spell_slots()
        points = level.points()
        bonus_damage = level.bonus_damage()
        increase_speed = level.increase_speed()
        return ReadClassLevelSchema(
            class_level_id=level.level_id(),
            class_id=level.class_id(),
            level=level.level(),
            dice=ClassLevelDiceSchema.from_domain(dice) if dice is not None else None,
            spell_slots=slots.slots() if slots is not None else None,
            number_cantrips_know=level.number_cantrips_know(),
            number_spells_know=level.number_spells_know(),
            number_arcanums_know=level.number_arcanums_know(),
            points=(
                ClassLevelPointsSchema.from_domain(points)
                if points is not None
                else None
            ),
            bonus_damage=(
                ClassLevelBonusDamageSchema.from_domain(bonus_damage)
                if bonus_damage is not None
                else None
            ),
            increase_speed=(
                ClassLevelIncreaseSpeedSchema.from_domain(increase_speed)
                if increase_speed is not None
                else None
            ),
        )


@dataclass
class CreateClassLevelSchema:
    level: int
    dice: ClassLevelDiceSchema | None
    spell_slots: Sequence[int] | None
    number_cantrips_know: int | None
    number_spells_know: int | None
    number_arcanums_know: int | None
    points: ClassLevelPointsSchema | None
    bonus_damage: ClassLevelBonusDamageSchema | None
    increase_speed: ClassLevelIncreaseSpeedSchema | None


@dataclass
class UpdateClassLevelSchema:
    class_id: UUID | None
    level: int | None
    dice: ClassLevelDiceSchema | None
    spell_slots: Sequence[int] | None
    number_cantrips_know: int | None
    number_spells_know: int | None
    number_arcanums_know: int | None
    points: ClassLevelPointsSchema | None
    bonus_damage: ClassLevelBonusDamageSchema | None
    increase_speed: ClassLevelIncreaseSpeedSchema | None
