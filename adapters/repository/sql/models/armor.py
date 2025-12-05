from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.armor import AppArmor, AppArmorClass
from application.dto.model.coin import AppCoins
from application.dto.model.weight import AppWeight
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.material import MaterialModel


class ArmorModel(Base):
    __tablename__ = "armor"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    armor_type: Mapped[str]
    strength: Mapped[int]
    stealth: Mapped[bool]
    weight: Mapped[float]
    cost: Mapped[int]
    base_class: Mapped[int]
    modifier: Mapped[str | None] = mapped_column(String(50))
    max_modifier_bonus: Mapped[int | None]
    material_id: Mapped[UUID] = mapped_column(ForeignKey("material.id"))

    material: Mapped["MaterialModel"] = relationship(back_populates="armors")

    def to_app(self) -> AppArmor:
        return AppArmor(
            armor_id=self.id,
            armor_type=self.armor_type,
            name=self.name,
            description=self.description,
            armor_class=AppArmorClass(
                base_class=self.base_class,
                modifier=self.modifier,
                max_modifier_bonus=self.max_modifier_bonus,
            ),
            strength=self.strength,
            stealth=self.stealth,
            weight=AppWeight(count=self.weight),
            cost=AppCoins(count=self.cost),
            material_id=self.material_id,
        )

    @staticmethod
    def from_app(armor: AppArmor) -> "ArmorModel":
        return ArmorModel(
            id=armor.armor_id,
            armor_type=armor.armor_type,
            name=armor.name,
            description=armor.description,
            armor_class=armor.armor_class.base_class,
            modifier=armor.armor_class.modifier,
            max_modifier_bonus=armor.armor_class.max_modifier_bonus,
            strength=armor.strength,
            stealth=armor.stealth,
            weight=armor.weight.count,
            cost=armor.cost.count,
            material_id=armor.material_id,
        )
