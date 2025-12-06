from dataclasses import dataclass
from uuid import UUID

from application.dto.command.material import (
    CreateMaterialCommand,
    UpdateMaterialCommand,
)
from application.dto.model.material import AppMaterial


@dataclass
class ReadMaterialSchema:
    material_id: UUID
    name: str
    description: str

    @staticmethod
    def from_app(material: AppMaterial) -> "ReadMaterialSchema":
        return ReadMaterialSchema(
            material_id=material.material_id,
            name=material.name,
            description=material.description,
        )


@dataclass
class CreateMaterialSchema:
    name: str
    description: str

    def to_command(self, user_id: UUID) -> CreateMaterialCommand:
        return CreateMaterialCommand(
            user_id=user_id, name=self.name, description=self.description
        )


@dataclass
class UpdateMaterialSchema:
    name: str | None = None
    description: str | None = None

    def to_command(self, user_id: UUID, material_id: UUID) -> UpdateMaterialCommand:
        return UpdateMaterialCommand(
            user_id=user_id,
            material_id=material_id,
            name=self.name,
            description=self.description,
        )
