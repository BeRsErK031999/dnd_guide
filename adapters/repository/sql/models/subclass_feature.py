from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from adapters.repository.sql.models.mixin import Timestamp
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_subclass import CharacterSubclass


class SubclassFeature(Timestamp, Base):
    __tablename__ = "subclass_feature"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    level: Mapped[int]
    character_subclass_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_subclass.id")
    )
    character_subclass: Mapped["CharacterSubclass"] = relationship(
        back_populates="features"
    )
