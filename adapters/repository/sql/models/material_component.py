from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
from adapters.repository.sql.models.mixin import Timestamp
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.spell import Spell


class MaterialComponent(Timestamp, Base):
    __tablename__ = "material_component"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    spells: Mapped[list["Spell"]] = relationship(
        back_populates="materials", secondary="rel_spell_material"
    )
