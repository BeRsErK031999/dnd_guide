from os import name
from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
from domain.material_component import MaterialComponent
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.spell import SpellModel


class MaterialComponentModel(Base):
    __tablename__ = "material_component"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]

    spells: Mapped[list[SpellModel]] = relationship(
        back_populates="materials", secondary="rel_spell_material"
    )

    def to_domain(self) -> MaterialComponent:
        return MaterialComponent(
            material_id=self.id,
            name=self.name,
            description=self.description,
        )

    @staticmethod
    def from_domain(material: MaterialComponent) -> MaterialComponentModel:
        return MaterialComponentModel(
            id=material.material_id(),
            name=material.name(),
            description=material.description(),
        )
