from dataclasses import dataclass
from uuid import UUID

from domain.weapon_property import WeaponProperty, WeaponPropertyName

from .dice import AppDice
from .length import AppLength

__all__ = [
    "AppWeaponProperty",
    "AppWeaponPropertyName",
]


@dataclass
class AppWeaponPropertyName:
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
    def from_domain() -> "AppWeaponPropertyName":
        return AppWeaponPropertyName(
            **{name.name.lower(): name.value for name in WeaponPropertyName}
        )


@dataclass
class AppWeaponProperty:
    weapon_property_id: UUID
    name: str
    description: str
    base_range: AppLength | None = None
    max_range: AppLength | None = None
    second_hand_dice: AppDice | None = None

    @staticmethod
    def from_domain(weapon_property: WeaponProperty) -> "AppWeaponProperty":
        base_range = weapon_property.base_range()
        max_range = weapon_property.max_range()
        second_hand_dice = weapon_property.second_hand_dice()
        return AppWeaponProperty(
            weapon_property_id=weapon_property.weapon_property_id(),
            name=weapon_property.name().name.lower(),
            description=weapon_property.description(),
            base_range=(
                AppLength.from_domain(base_range) if base_range is not None else None
            ),
            max_range=(
                AppLength.from_domain(max_range) if max_range is not None else None
            ),
            second_hand_dice=(
                AppDice.from_domain(second_hand_dice)
                if second_hand_dice is not None
                else None
            ),
        )

    def to_domain(self) -> WeaponProperty:
        return WeaponProperty(
            weapon_property_id=self.weapon_property_id,
            name=WeaponPropertyName.from_str(self.name),
            description=self.description,
            base_range=(
                self.base_range.to_domain() if self.base_range is not None else None
            ),
            max_range=(
                self.max_range.to_domain() if self.max_range is not None else None
            ),
            second_hand_dice=(
                self.second_hand_dice.to_domain()
                if self.second_hand_dice is not None
                else None
            ),
        )
