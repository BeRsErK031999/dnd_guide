from dataclasses import asdict, dataclass
from uuid import UUID

from application.dto.command.weapon_property import (
    CreateWeaponPropertyCommand,
    UpdateWeaponPropertyCommand,
    WeaponPropertyBaseRangeCommand,
    WeaponPropertyMaxRangeCommand,
    WeaponPropertySecondHandDiceCommand,
)
from application.dto.model.weapon_property import (
    AppWeaponProperty,
    AppWeaponPropertyName,
)
from ports.http.web.v1.schemas.dice import DiceSchema
from ports.http.web.v1.schemas.length import LengthSchema


@dataclass
class ReadWeaponPropertyNameSchema:
    ammunition: str
    finesse: str
    heavy: str
    light: str
    reach: str
    special: str
    thrown: str
    two_handed: str
    versatile: str
    distance: str

    @staticmethod
    def from_domain() -> "ReadWeaponPropertyNameSchema":
        return ReadWeaponPropertyNameSchema(
            **asdict(AppWeaponPropertyName.from_domain())
        )


@dataclass
class WeaponPropertyBaseRangeSchema:
    range: LengthSchema | None

    def to_command(self) -> WeaponPropertyBaseRangeCommand:
        return WeaponPropertyBaseRangeCommand(
            range=self.range.to_command() if self.range is not None else None
        )


@dataclass
class WeaponPropertyMaxRangeSchema:
    range: LengthSchema | None

    def to_command(self) -> WeaponPropertyMaxRangeCommand:
        return WeaponPropertyMaxRangeCommand(
            range=self.range.to_command() if self.range is not None else None
        )


@dataclass
class WeaponPropertySecondHandDiceSchema:
    dice: DiceSchema | None

    def to_command(self) -> WeaponPropertySecondHandDiceCommand:
        return WeaponPropertySecondHandDiceCommand(
            dice=self.dice.to_command() if self.dice is not None else None
        )


@dataclass
class ReadWeaponPropertySchema:
    weapon_property_id: UUID
    name: str
    description: str
    base_range: LengthSchema | None = None
    max_range: LengthSchema | None = None
    second_hand_dice: DiceSchema | None = None

    @staticmethod
    def from_app(weapon_property: AppWeaponProperty) -> "ReadWeaponPropertySchema":
        return ReadWeaponPropertySchema(
            weapon_property_id=weapon_property.weapon_property_id,
            name=weapon_property.name,
            description=weapon_property.description,
            base_range=(
                LengthSchema.from_app(weapon_property.base_range)
                if weapon_property.base_range is not None
                else None
            ),
            max_range=(
                LengthSchema.from_app(weapon_property.max_range)
                if weapon_property.max_range is not None
                else None
            ),
            second_hand_dice=(
                DiceSchema.from_app(weapon_property.second_hand_dice)
                if weapon_property.second_hand_dice is not None
                else None
            ),
        )


@dataclass
class CreateWeaponPropertySchema:
    name: str
    description: str
    base_range: WeaponPropertyBaseRangeSchema | None = None
    max_range: WeaponPropertyMaxRangeSchema | None = None
    second_hand_dice: WeaponPropertySecondHandDiceSchema | None = None

    def to_command(self, user_id: UUID) -> CreateWeaponPropertyCommand:
        return CreateWeaponPropertyCommand(
            user_id=user_id,
            name=self.name,
            description=self.description,
            base_range=(
                self.base_range.to_command() if self.base_range is not None else None
            ),
            max_range=(
                self.max_range.to_command() if self.max_range is not None else None
            ),
            second_hand_dice=(
                self.second_hand_dice.to_command()
                if self.second_hand_dice is not None
                else None
            ),
        )


@dataclass
class UpdateWeaponPropertySchema:
    name: str | None = None
    description: str | None = None
    base_range: WeaponPropertyBaseRangeSchema | None = None
    max_range: WeaponPropertyMaxRangeSchema | None = None
    second_hand_dice: WeaponPropertySecondHandDiceSchema | None = None

    def to_command(
        self, user_id: UUID, property_id: UUID
    ) -> UpdateWeaponPropertyCommand:
        return UpdateWeaponPropertyCommand(
            user_id=user_id,
            weapon_property_id=property_id,
            name=self.name,
            description=self.description,
            base_range=(
                self.base_range.to_command() if self.base_range is not None else None
            ),
            max_range=(
                self.max_range.to_command() if self.max_range is not None else None
            ),
            second_hand_dice=(
                self.second_hand_dice.to_command()
                if self.second_hand_dice is not None
                else None
            ),
        )
