from dataclasses import dataclass
from uuid import UUID

from domain.material_component import MaterialComponent

__all__ = ["AppMaterialComponent"]


@dataclass
class AppMaterialComponent:
    material_id: UUID
    name: str
    description: str

    @staticmethod
    def from_domain(material: MaterialComponent) -> "AppMaterialComponent":
        return AppMaterialComponent(
            material_id=material.material_id(),
            name=material.name(),
            description=material.description(),
        )

    def to_domain(self) -> MaterialComponent:
        return MaterialComponent(
            material_id=self.material_id,
            name=self.name,
            description=self.description,
        )
