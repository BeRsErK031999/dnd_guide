from dataclasses import dataclass
from uuid import UUID

from domain.material_component import MaterialComponent
from litestar.dto import DataclassDTO


@dataclass
class ReadMaterialComponentSchema:
    material_id: UUID
    name: str
    description: str

    @staticmethod
    def from_domain(material: MaterialComponent) -> ReadMaterialComponentSchema:
        return ReadMaterialComponentSchema(
            material_id=material.material_id(),
            name=material.name(),
            description=material.description(),
        )


@dataclass
class CreateMaterialComponentSchema:
    name: str
    description: str


class CreateMaterialComponentDTO(DataclassDTO[CreateMaterialComponentSchema]):
    pass


@dataclass
class UpdateMaterialComponentSchema:
    name: str | None
    description: str | None


class UpdateMaterialComponentDTO(DataclassDTO[UpdateMaterialComponentSchema]):
    pass
