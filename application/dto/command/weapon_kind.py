from dataclasses import dataclass
from uuid import UUID

from domain.error import DomainError


@dataclass
class CreateWeaponKindCommand:
    user_id: UUID
    weapon_type: str
    name: str
    description: str


@dataclass
class UpdateWeaponKindCommand:
    user_id: UUID
    weapon_kind_id: UUID
    weapon_type: str | None = None
    name: str | None = None
    description: str | None = None

    def __post_init__(self) -> None:
        if all([self.weapon_type is None, self.name is None, self.description is None]):
            raise DomainError.invalid_data(
                "не переданы данные для обновления вида оружия"
            )


@dataclass
class DeleteWeaponKindCommand:
    user_id: UUID
    weapon_kind_id: UUID
