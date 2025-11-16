from typing import TYPE_CHECKING

from adapters.repository.sql.models.base import Base
from domain.creature_size import CreatureSize
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.race import RaceModel


class CreatureSizeModel(Base):
    __tablename__ = "creature_size"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]

    races: Mapped[list["RaceModel"]] = relationship(back_populates="creature_size")

    def to_domain(self) -> CreatureSize:
        return CreatureSize(
            size_id=self.id,
            name=self.name,
            description=self.description,
        )

    @staticmethod
    def from_domain(size: CreatureSize) -> "CreatureSizeModel":
        return CreatureSizeModel(
            id=size.size_id(),
            name=size.name(),
            description=size.description(),
        )
