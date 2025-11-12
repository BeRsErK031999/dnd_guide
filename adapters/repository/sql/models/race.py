from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.creature_size import CreatureSizeModel
    from adapters.repository.sql.models.creature_type import CreatureTypeModel
    from adapters.repository.sql.models.source import SourceModel


class RaceModel(Base):
    __tablename__ = "race"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    base_speed: Mapped[int]
    speed_description: Mapped[str]
    max_age: Mapped[int]
    age_description: Mapped[str]
    creature_type_id: Mapped[UUID] = mapped_column(ForeignKey("creature_type.id"))
    creature_type: Mapped["CreatureTypeModel"] = relationship(back_populates="races")
    creature_size_id: Mapped[UUID] = mapped_column(ForeignKey("creature_size.id"))
    creature_size: Mapped["CreatureSizeModel"] = relationship(back_populates="races")
    increase_modifiers: Mapped[list[RaceIncreaseModifierModel]] = relationship(
        back_populates="race"
    )
    features: Mapped[list[RaceFeatureModel]] = relationship(back_populates="race")
    source_id: Mapped[UUID] = mapped_column(ForeignKey("source.id"))
    source: Mapped[SourceModel] = relationship(back_populates="races")


class RaceIncreaseModifierModel(Base):
    __tablename__ = "race_increase_modifier"

    name: Mapped[str] = mapped_column(String(50))
    bonus: Mapped[int]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped[RaceModel] = relationship(back_populates="increase_modifiers")


class RaceFeatureModel(Base):
    __tablename__ = "race_feature"

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped[RaceModel] = relationship(back_populates="features")
