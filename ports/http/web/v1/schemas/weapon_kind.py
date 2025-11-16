from dataclasses import dataclass
from uuid import UUID

from domain.weapon_kind import WeaponKind, WeaponType


@dataclass
class ReadWeaponTypeSchema:
    simple_range: str
    simple_melee: str
    martial_range: str
    martial_melee: str

    @staticmethod
    def from_domain() -> "ReadWeaponTypeSchema":
        return ReadWeaponTypeSchema(
            **{
                weapon_type.name.lower(): weapon_type.value
                for weapon_type in WeaponType
            }
        )


@dataclass
class ReadWeaponKindSchema:
    weapon_kind_id: UUID
    weapon_type: str
    name: str
    description: str

    @staticmethod
    def from_domain(weapon_kind: WeaponKind) -> "ReadWeaponKindSchema":
        return ReadWeaponKindSchema(
            weapon_kind_id=weapon_kind.weapon_kind_id(),
            weapon_type=weapon_kind.weapon_type(),
            name=weapon_kind.name(),
            description=weapon_kind.description(),
        )


@dataclass
class CreateWeaponKindSchema:
    weapon_type: str
    name: str
    description: str


@dataclass
class UpdateWeaponKindSchema:
    weapon_type: str | None = None
    name: str | None = None
    description: str | None = None
