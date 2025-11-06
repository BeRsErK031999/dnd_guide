from dataclasses import dataclass
from uuid import UUID

from application.dto.command.dice import DiceCommand
from application.dto.command.length import LengthCommand


@dataclass
class WeaponPropertyBaseRangeCommand:
    range: LengthCommand | None


@dataclass
class WeaponPropertyMaxRangeCommand:
    range: LengthCommand | None


@dataclass
class WeaponPropertySecondHandDiceCommand:
    dice: DiceCommand | None


@dataclass
class CreateWeaponPropertyCommand:
    user_id: UUID
    name: str
    description: str
    base_range: WeaponPropertyBaseRangeCommand | None = None
    max_range: WeaponPropertyMaxRangeCommand | None = None
    second_hand_dice: WeaponPropertySecondHandDiceCommand | None = None


@dataclass
class UpdateWeaponPropertyCommand:
    user_id: UUID
    weapon_property_id: UUID
    name: str | None = None
    description: str | None = None
    base_range: WeaponPropertyBaseRangeCommand | None = None
    max_range: WeaponPropertyMaxRangeCommand | None = None
    second_hand_dice: WeaponPropertySecondHandDiceCommand | None = None


@dataclass
class DeleteWeaponPropertyCommand:
    user_id: UUID
    weapon_property_id: UUID
