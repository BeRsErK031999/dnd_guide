from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
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
