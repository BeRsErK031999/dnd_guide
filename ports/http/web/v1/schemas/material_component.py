from dataclasses import dataclass
from uuid import UUID

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


@dataclass
class UpdateMaterialComponentSchema:
    name: str | None = None
    description: str | None = None
