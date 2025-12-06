from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.model.class_level import (
    AppClassLevel,
    AppClassLevelBonusDamage,
    AppClassLevelDice,
    AppClassLevelIncreaseSpeed,
    AppClassLevelPoints,
)
from ports.http.web.v1.schemas.dice import DiceSchema
from ports.http.web.v1.schemas.length import LengthSchema


@dataclass
class ClassLevelDiceSchema:
    dice: DiceSchema
    description: str

    @staticmethod
    def from_app(level_dice: AppClassLevelDice) -> "ClassLevelDiceSchema":
        return ClassLevelDiceSchema(
            dice=DiceSchema.from_app(level_dice.dice),
            description=level_dice.description,
        )


@dataclass
class ClassLevelPointsSchema:
    points: int
    description: str

    @staticmethod
    def from_app(level_points: AppClassLevelPoints) -> "ClassLevelPointsSchema":
        return ClassLevelPointsSchema(
            points=level_points.points,
            description=level_points.description,
        )


@dataclass
class ClassLevelBonusDamageSchema:
    damage: int
    description: str

    @staticmethod
    def from_app(
        level_bonus_damage: AppClassLevelBonusDamage,
    ) -> "ClassLevelBonusDamageSchema":
        return ClassLevelBonusDamageSchema(
            damage=level_bonus_damage.damage,
            description=level_bonus_damage.description,
        )


@dataclass
class ClassLevelIncreaseSpeedSchema:
    speed: LengthSchema
    description: str

    @staticmethod
    def from_app(
        level_increase_speed: AppClassLevelIncreaseSpeed,
    ) -> "ClassLevelIncreaseSpeedSchema":
        return ClassLevelIncreaseSpeedSchema(
            speed=LengthSchema.from_app(level_increase_speed.speed),
            description=level_increase_speed.description,
        )


@dataclass
class ReadClassLevelSchema:
    class_level_id: UUID
    class_id: UUID
    level: int
    dice: ClassLevelDiceSchema | None = None
    spell_slots: Sequence[int] | None = None
    number_cantrips_know: int | None = None
    number_spells_know: int | None = None
    number_arcanums_know: int | None = None
    points: ClassLevelPointsSchema | None = None
    bonus_damage: ClassLevelBonusDamageSchema | None = None
    increase_speed: ClassLevelIncreaseSpeedSchema | None = None

    @staticmethod
    def from_app(level: AppClassLevel) -> "ReadClassLevelSchema":
        dice = level.dice
        points = level.points
        bonus_damage = level.bonus_damage
        increase_speed = level.increase_speed
        return ReadClassLevelSchema(
            class_level_id=level.class_level_id,
            class_id=level.class_id,
            level=level.level,
            dice=(
                ClassLevelDiceSchema.from_app(level.dice)
                if level.dice is not None
                else None
            ),
            spell_slots=level.spell_slots,
            number_cantrips_know=level.number_cantrips_know,
            number_spells_know=level.number_spells_know,
            number_arcanums_know=level.number_arcanums_know,
            points=(
                ClassLevelPointsSchema.from_app(points) if points is not None else None
            ),
            bonus_damage=(
                ClassLevelBonusDamageSchema.from_app(bonus_damage)
                if bonus_damage is not None
                else None
            ),
            increase_speed=(
                ClassLevelIncreaseSpeedSchema.from_app(increase_speed)
                if increase_speed is not None
                else None
            ),
        )


@dataclass
class CreateClassLevelSchema:
    level: int
    dice: ClassLevelDiceSchema | None = None
    spell_slots: Sequence[int] | None = None
    number_cantrips_know: int | None = None
    number_spells_know: int | None = None
    number_arcanums_know: int | None = None
    points: ClassLevelPointsSchema | None = None
    bonus_damage: ClassLevelBonusDamageSchema | None = None
    increase_speed: ClassLevelIncreaseSpeedSchema | None = None


@dataclass
class UpdateClassLevelSchema:
    class_id: UUID | None = None
    level: int | None = None
    dice: ClassLevelDiceSchema | None = None
    spell_slots: Sequence[int] | None = None
    number_cantrips_know: int | None = None
    number_spells_know: int | None = None
    number_arcanums_know: int | None = None
    points: ClassLevelPointsSchema | None = None
    bonus_damage: ClassLevelBonusDamageSchema | None = None
    increase_speed: ClassLevelIncreaseSpeedSchema | None = None
