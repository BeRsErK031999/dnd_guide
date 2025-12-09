from dataclasses import dataclass
from uuid import UUID

from domain.error import DomainError

__all__ = [
    "CreateMaterialComponentCommand",
    "UpdateMaterialComponentCommand",
    "DeleteMaterialComponentCommand",
]


@dataclass
class CreateMaterialComponentCommand:
    user_id: UUID
    name: str
    description: str


@dataclass
class UpdateMaterialComponentCommand:
    user_id: UUID
    material_id: UUID
    name: str | None
    description: str | None

    def __post_init__(self) -> None:
        if all([self.name is None, self.description is None]):
            raise DomainError.invalid_data(
                "не переданы данные для обновления материала"
            )


@dataclass
class DeleteMaterialComponentCommand:
    user_id: UUID
    material_id: UUID
