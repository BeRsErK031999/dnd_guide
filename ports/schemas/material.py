from dataclasses import dataclass

from domain.material import Material
from litestar.dto import DataclassDTO


@dataclass
class ReadMaterialSchema:
    name: str
    description: str

    @staticmethod
    def from_domain(material: Material) -> ReadMaterialSchema:
        return ReadMaterialSchema(
            name=material.name(),
            description=material.description(),
        )


@dataclass
class CreateMaterialSchema:
    name: str
    description: str


class CreateMaterialDTO(DataclassDTO[CreateMaterialSchema]):
    pass


@dataclass
class UpdateMaterialSchema:
    name: str | None
    description: str | None


class UpdateMaterialDTO(DataclassDTO[CreateMaterialSchema]):
    pass
