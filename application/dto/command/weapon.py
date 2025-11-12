from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.command.coin import CoinCommand
from application.dto.command.dice import DiceCommand
from application.dto.command.weight import WeightCommand
from domain.error import DomainError


@dataclass
class WeaponDamageCommand:
    dice: DiceCommand
    damage_type: str
    bonus_damage: int


@dataclass
class CreateWeaponCommand:
    user_id: UUID
    weapon_kind_id: UUID
    name: str
    description: str
    cost: CoinCommand
    damage: WeaponDamageCommand
    weight: WeightCommand
    weapon_property_ids: Sequence[UUID]
    material_id: UUID


@dataclass
class UpdateWeaponCommand:
    user_id: UUID
    weapon_id: UUID
    weapon_kind_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    cost: CoinCommand | None = None
    damage: WeaponDamageCommand | None = None
    weight: WeightCommand | None = None
    weapon_property_ids: Sequence[UUID] | None = None
    material_id: UUID | None = None

    def __post_init__(self):
        if all(
            [
                self.weapon_kind_id is None,
                self.name is None,
                self.description is None,
                self.cost is None,
                self.damage is None,
                self.weight is None,
                self.weapon_property_ids is None,
                self.material_id is None,
            ]
        ):
            raise DomainError.invalid_data("не переданы данные для обновления оружия")


@dataclass
class DeleteWeaponCommand:
    user_id: UUID
    weapon_id: UUID
