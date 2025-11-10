from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from adapters.repository.sql.models.mixin import Timestamp
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.creature_size import CreatureSize
    from adapters.repository.sql.models.creature_type import CreatureType


class Race(Timestamp, Base):
    __tablename__ = "race"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(100))
    base_speed: Mapped[int]
    speed_description: Mapped[str]
    max_age: Mapped[int]
    age_description: Mapped[str]
    creature_type_id: Mapped[UUID] = mapped_column(ForeignKey("creature_type.id"))
    creature_type: Mapped["CreatureType"] = relationship(back_populates="races")
    creature_size_id: Mapped[UUID] = mapped_column(ForeignKey("creature_size.id"))
    creature_size: Mapped["CreatureSize"] = relationship(back_populates="races")
    increase_modifiers: Mapped[list["RaceIncreaseModifier"]] = relationship(
        back_populates="race"
    )
    features: Mapped[list["RaceFeature"]] = relationship(back_populates="race")


class RaceIncreaseModifier(Timestamp, Base):
    __tablename__ = "race_increase_modifier"

    name: Mapped[str] = mapped_column(String(100))
    bonus: Mapped[int]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped["Race"] = relationship(back_populates="increase_modifiers")


class RaceFeature(Timestamp, Base):
    __tablename__ = "race_feature"

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped["Race"] = relationship(back_populates="features")
