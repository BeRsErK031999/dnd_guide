from dataclasses import dataclass
from uuid import UUID

__all__ = [
    "CreateMaterialCommand",
    "UpdateMaterialCommand",
    "DeleteMaterialCommand",
]


@dataclass
class CreateMaterialCommand:
    user_id: UUID
    name: str
    description: str


@dataclass
class UpdateMaterialCommand:
    user_id: UUID
    material_id: UUID
    name: str | None = None
    description: str | None = None


@dataclass
class DeleteMaterialCommand:
    user_id: UUID
    material_id: UUID
