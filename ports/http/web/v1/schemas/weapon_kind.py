from dataclasses import dataclass
from uuid import UUID

from domain.weapon_kind import WeaponKind
from litestar.dto import DataclassDTO


@dataclass
class ReadWeaponKindSchema:
    weapon_kind_id: UUID
    weapon_type: str
    name: str
    description: str

    @staticmethod
    def from_domain(weapon_kind: WeaponKind) -> ReadWeaponKindSchema:
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


class CreateWeaponKindDTO(DataclassDTO[CreateWeaponKindSchema]):
    pass


@dataclass
class UpdateWeaponKindSchema:
    weapon_type: str | None = None
    name: str | None = None
    description: str | None = None


class UpdateWeaponKindDTO(DataclassDTO[UpdateWeaponKindSchema]):
    pass
