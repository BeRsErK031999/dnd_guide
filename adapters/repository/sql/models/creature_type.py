from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
from domain.creature_type import CreatureType
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.race import RaceModel


class CreatureTypeModel(Base):
    __tablename__ = "creature_type"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]

    races: Mapped[list[RaceModel]] = relationship(back_populates="creature_type")

    def to_domain(self) -> CreatureType:
        return CreatureType(
            type_id=self.id,
            name=self.name,
            description=self.description,
        )

    @staticmethod
    def from_domain(size: CreatureType) -> CreatureTypeModel:
        return CreatureTypeModel(
            id=size.type_id(),
            name=size.name(),
            description=size.description(),
        )
