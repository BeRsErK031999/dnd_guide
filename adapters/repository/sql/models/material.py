from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
from application.dto.model.material import AppMaterial
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.armor import ArmorModel
    from adapters.repository.sql.models.weapon import WeaponModel


class MaterialModel(Base):
    __tablename__ = "material"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]

    armors: Mapped[list["ArmorModel"]] = relationship(back_populates="material")
    weapons: Mapped[list["WeaponModel"]] = relationship(back_populates="material")

    def to_app(self) -> "AppMaterial":
        return AppMaterial(
            material_id=self.id,
            name=self.name,
            description=self.description,
        )

    @staticmethod
    def from_app(material: AppMaterial) -> "MaterialModel":
        return MaterialModel(
            id=material.material_id,
            name=material.name,
            description=material.description,
        )
