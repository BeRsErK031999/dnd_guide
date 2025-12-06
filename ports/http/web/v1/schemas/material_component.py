from dataclasses import dataclass
from uuid import UUID

from application.dto.command.material_component import (
    CreateMaterialComponentCommand,
    UpdateMaterialComponentCommand,
)
from application.dto.model.material_component import AppMaterialComponent


@dataclass
class ReadMaterialComponentSchema:
    material_id: UUID
    name: str
    description: str

    @staticmethod
    def from_app(material: AppMaterialComponent) -> "ReadMaterialComponentSchema":
        return ReadMaterialComponentSchema(
            material_id=material.material_id,
            name=material.name,
            description=material.description,
        )


@dataclass
class CreateMaterialComponentSchema:
    name: str
    description: str

    def to_command(self, user_id: UUID) -> CreateMaterialComponentCommand:
        return CreateMaterialComponentCommand(
            user_id=user_id, name=self.name, description=self.description
        )


@dataclass
class UpdateMaterialComponentSchema:
    name: str | None = None
    description: str | None = None

    def to_command(
        self, user_id: UUID, material_id: UUID
    ) -> UpdateMaterialComponentCommand:
        return UpdateMaterialComponentCommand(
            user_id=user_id,
            material_id=material_id,
            name=self.name,
            description=self.description,
        )
