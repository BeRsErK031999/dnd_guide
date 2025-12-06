from dataclasses import dataclass
from uuid import UUID

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


@dataclass
class UpdateMaterialSchema:
    name: str | None = None
    description: str | None = None
