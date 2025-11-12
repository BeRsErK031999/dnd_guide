from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_class import CharacterClassModel


class ClassFeatureModel(Base):
    __tablename__ = "class_feature"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    level: Mapped[int]
    character_class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped[CharacterClassModel] = relationship(
        back_populates="features"
    )
