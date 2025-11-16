from dataclasses import dataclass

from domain.material import Material


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


@dataclass
class UpdateMaterialSchema:
    name: str | None
    description: str | None
