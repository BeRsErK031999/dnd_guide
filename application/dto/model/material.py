from dataclasses import dataclass
from uuid import UUID

from domain.material import Material

__all__ = ["AppMaterial"]


@dataclass
class AppMaterial:
    material_id: UUID
    name: str
    description: str

    @staticmethod
    def from_domain(material: Material) -> "AppMaterial":
        return AppMaterial(
            material_id=material.material_id(),
            name=material.name(),
            description=material.description(),
        )

    def to_domain(self) -> Material:
        return Material(
            material_id=self.material_id,
            name=self.name,
            description=self.description,
        )
