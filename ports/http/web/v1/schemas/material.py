from dataclasses import dataclass
from uuid import UUID

from domain.material import Material


@dataclass
class ReadMaterialSchema:
    material_id: UUID
    name: str
    description: str

    @staticmethod
    def from_domain(material: Material) -> "ReadMaterialSchema":
        return ReadMaterialSchema(
            material_id=material.material_id(),
            name=material.name(),
            description=material.description(),
        )


@dataclass
class CreateMaterialSchema:
    name: str
    description: str


@dataclass
class UpdateMaterialSchema:
    name: str | None
    description: str | None
