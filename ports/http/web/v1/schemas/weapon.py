from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.model.weapon import AppWeapon, AppWeaponDamage
from ports.http.web.v1.schemas.coin import CoinSchema
from ports.http.web.v1.schemas.dice import DiceSchema
from ports.http.web.v1.schemas.weight import WeightSchema


@dataclass
class WeaponDamageSchema:
    dice: DiceSchema
    damage_type: str
    bonus_damage: int

    @staticmethod
    def from_app(weapon_damage: AppWeaponDamage) -> "WeaponDamageSchema":
        return WeaponDamageSchema(
            dice=DiceSchema.from_app(weapon_damage.dice),
            damage_type=weapon_damage.damage_type,
            bonus_damage=weapon_damage.bonus_damage,
        )


@dataclass
class ReadWeaponSchema:
    weapon_id: UUID
    weapon_kind_id: UUID
    name: str
    description: str
    cost: CoinSchema
    damage: WeaponDamageSchema
    weight: WeightSchema
    weapon_property_ids: Sequence[UUID]
    material_id: UUID

    @staticmethod
    def from_app(weapon: AppWeapon) -> "ReadWeaponSchema":
        return ReadWeaponSchema(
            weapon_id=weapon.weapon_id,
            weapon_kind_id=weapon.weapon_kind_id,
            name=weapon.name,
            description=weapon.description,
            cost=CoinSchema.from_app(weapon.cost),
            damage=WeaponDamageSchema.from_app(weapon.damage),
            weight=WeightSchema.from_app(weapon.weight),
            weapon_property_ids=weapon.weapon_property_ids,
            material_id=weapon.material_id,
        )


@dataclass
class CreateWeaponSchema:
    weapon_kind_id: UUID
    name: str
    description: str
    cost: CoinSchema
    damage: WeaponDamageSchema
    weight: WeightSchema
    weapon_property_ids: Sequence[UUID]
    material_id: UUID


@dataclass
class UpdateWeaponSchema:
    weapon_kind_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    cost: CoinSchema | None = None
    damage: WeaponDamageSchema | None = None
    weight: WeightSchema | None = None
    weapon_property_ids: Sequence[UUID] | None = None
    material_id: UUID | None = None
