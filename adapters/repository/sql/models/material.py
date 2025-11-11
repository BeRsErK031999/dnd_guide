from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.armor import Armor
    from adapters.repository.sql.models.weapon import Weapon


class Material(Base):
    __tablename__ = "material"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    armors: Mapped[list["Armor"]] = relationship(back_populates="material")
    weapons: Mapped[list["Weapon"]] = relationship(back_populates="material")
