from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.command.class_level import (
    ClassLevelBonusDamageCommand,
    ClassLevelDiceCommand,
    ClassLevelIncreaseSpeedCommand,
    ClassLevelPointsCommand,
    CreateClassLevelCommand,
    UpdateClassLevelCommand,
)
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

    def to_command(self) -> ClassLevelDiceCommand:
        return ClassLevelDiceCommand(
            dice=self.dice.to_command(), description=self.description
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

    def to_command(self) -> ClassLevelPointsCommand:
        return ClassLevelPointsCommand(points=self.points, description=self.description)


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

    def to_command(self) -> ClassLevelBonusDamageCommand:
        return ClassLevelBonusDamageCommand(
            damage=self.damage, description=self.description
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

    def to_command(self) -> ClassLevelIncreaseSpeedCommand:
        return ClassLevelIncreaseSpeedCommand(
            speed=self.speed.to_command(), description=self.description
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

    def to_command(self, user_id: UUID) -> CreateClassLevelCommand:
        return CreateClassLevelCommand(
            user_id=user_id,
            class_id=self.class_id,
            level=self.level,
            dice=self.dice.to_command() if self.dice is not None else None,
            spell_slots=self.spell_slots,
            number_cantrips_know=self.number_cantrips_know,
            number_spells_know=self.number_spells_know,
            number_arcanums_know=self.number_arcanums_know,
            points=self.points.to_command() if self.points is not None else None,
            bonus_damage=(
                self.bonus_damage.to_command()
                if self.bonus_damage is not None
                else None
            ),
            increase_speed=(
                self.increase_speed.to_command()
                if self.increase_speed is not None
                else None
            ),
        )


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

    def to_command(self, user_id: UUID, level_id: UUID) -> UpdateClassLevelCommand:
        return UpdateClassLevelCommand(
            user_id=user_id,
            class_level_id=level_id,
            class_id=self.class_id,
            level=self.level,
            dice=self.dice.to_command() if self.dice is not None else None,
            spell_slots=self.spell_slots,
            number_cantrips_know=self.number_cantrips_know,
            number_spells_know=self.number_spells_know,
            number_arcanums_know=self.number_arcanums_know,
            points=self.points.to_command() if self.points is not None else None,
            bonus_damage=(
                self.bonus_damage.to_command()
                if self.bonus_damage is not None
                else None
            ),
            increase_speed=(
                self.increase_speed.to_command()
                if self.increase_speed is not None
                else None
            ),
        )
