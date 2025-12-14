from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.damage_type import DamageType
from domain.weapon import Weapon, WeaponDamage

from .coin import AppCoins
from .dice import AppDice
from .weight import AppWeight

__all__ = ["AppWeapon", "AppWeaponDamage"]


@dataclass
class AppWeaponDamage:
    dice: AppDice
    damage_type: str
    bonus_damage: int

    @staticmethod
    def from_domain(weapon_damage: WeaponDamage) -> "AppWeaponDamage":
        return AppWeaponDamage(
            dice=AppDice.from_domain(weapon_damage.dice()),
            damage_type=weapon_damage.damage_type().name.lower(),
            bonus_damage=weapon_damage.bonus_damage(),
        )

    def to_domain(self) -> WeaponDamage:
        return WeaponDamage(
            dice=self.dice.to_domain(),
            damage_type=DamageType.from_str(self.damage_type),
            bonus_damage=self.bonus_damage,
        )


@dataclass
class AppWeapon:
    weapon_id: UUID
    weapon_kind_id: UUID
    name: str
    description: str
    cost: AppCoins
    damage: AppWeaponDamage
    weight: AppWeight
    weapon_property_ids: Sequence[UUID]
    material_id: UUID

    @staticmethod
    def from_domain(weapon: Weapon) -> "AppWeapon":
        return AppWeapon(
            weapon_id=weapon.weapon_id(),
            weapon_kind_id=weapon.kind_id(),
            name=weapon.name(),
            description=weapon.description(),
            cost=AppCoins.from_domain(weapon.cost()),
            damage=AppWeaponDamage.from_domain(weapon.damage()),
            weight=AppWeight.from_domain(weapon.weight()),
            weapon_property_ids=weapon.property_ids(),
            material_id=weapon.material_id(),
        )

    def to_domain(self) -> Weapon:
        return Weapon(
            weapon_id=self.weapon_id,
            weapon_kind_id=self.weapon_kind_id,
            name=self.name,
            description=self.description,
            cost=self.cost.to_domain(),
            damage=self.damage.to_domain(),
            weight=self.weight.to_domain(),
            weapon_property_ids=self.weapon_property_ids,
            material_id=self.material_id,
        )
