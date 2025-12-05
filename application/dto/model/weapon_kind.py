from dataclasses import dataclass
from uuid import UUID

from domain.weapon_kind import WeaponKind, WeaponType


@dataclass
class AppWeaponType:
    simple_range: str
    simple_melee: str
    martial_range: str
    martial_melee: str

    @staticmethod
    def from_domain() -> "AppWeaponType":
        return AppWeaponType(
            **{
                weapon_type.name.lower(): weapon_type.value
                for weapon_type in WeaponType
            }
        )


@dataclass
class AppWeaponKind:
    weapon_kind_id: UUID
    weapon_type: str
    name: str
    description: str

    @staticmethod
    def from_domain(weapon_kind: WeaponKind) -> "AppWeaponKind":
        return AppWeaponKind(
            weapon_kind_id=weapon_kind.weapon_kind_id(),
            weapon_type=weapon_kind.weapon_type(),
            name=weapon_kind.name(),
            description=weapon_kind.description(),
        )

    def to_domain(self) -> WeaponKind:
        return WeaponKind(
            weapon_kind_id=self.weapon_kind_id,
            weapon_type=WeaponType.from_str(self.weapon_type),
            name=self.name,
            description=self.description,
        )
