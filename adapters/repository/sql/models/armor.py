from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.armor import Armor, ArmorClass, ArmorType
from domain.coin import Coins, PieceType
from domain.modifier import Modifier
from domain.weight import Weight, WeightUnit
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

    def to_domain(self) -> Armor:
        return Armor(
            armor_id=self.id,
            armor_type=ArmorType.from_str(self.armor_type),
            name=self.name,
            description=self.description,
            armor_class=ArmorClass(
                self.base_class,
                Modifier.from_str(self.modifier) if self.modifier is not None else None,
                (
                    self.max_modifier_bonus
                    if self.max_modifier_bonus is not None
                    else None
                ),
            ),
            strength=self.strength,
            stealth=self.stealth,
            weight=Weight(self.weight, WeightUnit.LB),
            cost=Coins(self.cost, PieceType.COPPER),
            material_id=self.material_id,
        )

    @staticmethod
    def from_domain(armor: Armor) -> "ArmorModel":
        modifier = armor.armor_class().modifier()
        max_modifier_bonus = armor.armor_class().max_modifier_bonus()
        return ArmorModel(
            id=armor.armor_id(),
            name=armor.name(),
            description=armor.description(),
            armor_type=armor.armor_type().name,
            strength=armor.strength(),
            stealth=armor.stealth(),
            weight=armor.weight().in_lb(),
            cost=armor.cost().in_copper(),
            base_class=armor.armor_class().base_class(),
            modifier=modifier.name if modifier is not None else None,
            max_modifier_bonus=(
                max_modifier_bonus if max_modifier_bonus is not None else None
            ),
            material_id=armor.material_id(),
        )
