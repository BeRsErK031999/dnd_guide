from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.material import Material


class Armor(Base):
    __tablename__ = "armor"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    armor_type: Mapped[str]
    strength: Mapped[int]
    stealth: Mapped[bool]
    weight: Mapped[float]
    cost: Mapped[float]
    base_class: Mapped[int]
    modifier: Mapped[str] = mapped_column(String(50), nullable=True)
    max_modifier_bonus: Mapped[int | None]
    material_id: Mapped[UUID] = mapped_column(ForeignKey("material.id"))
    material: Mapped["Material"] = relationship(back_populates="armors")
