from dataclasses import asdict, dataclass
from uuid import UUID

from application.dto.command.weapon_kind import (
    CreateWeaponKindCommand,
    UpdateWeaponKindCommand,
)
from application.dto.model.weapon_kind import AppWeaponKind, AppWeaponType


@dataclass
class ReadWeaponTypeSchema:
    simple_range: str
    simple_melee: str
    martial_range: str
    martial_melee: str

    @staticmethod
    def from_domain() -> "ReadWeaponTypeSchema":
        return ReadWeaponTypeSchema(**asdict(AppWeaponType.from_domain()))


@dataclass
class ReadWeaponKindSchema:
    weapon_kind_id: UUID
    weapon_type: str
    name: str
    description: str

    @staticmethod
    def from_app(weapon_kind: AppWeaponKind) -> "ReadWeaponKindSchema":
        return ReadWeaponKindSchema(
            weapon_kind_id=weapon_kind.weapon_kind_id,
            weapon_type=weapon_kind.weapon_type,
            name=weapon_kind.name,
            description=weapon_kind.description,
        )


@dataclass
class CreateWeaponKindSchema:
    weapon_type: str
    name: str
    description: str

    def to_command(self, user_id: UUID) -> CreateWeaponKindCommand:
        return CreateWeaponKindCommand(
            user_id=user_id,
            weapon_type=self.weapon_type,
            name=self.name,
            description=self.description,
        )


@dataclass
class UpdateWeaponKindSchema:
    weapon_type: str | None = None
    name: str | None = None
    description: str | None = None

    def to_command(self, user_id: UUID, kind_id: UUID) -> UpdateWeaponKindCommand:
        return UpdateWeaponKindCommand(
            user_id=user_id,
            weapon_kind_id=kind_id,
            weapon_type=self.weapon_type,
            name=self.name,
            description=self.description,
        )
