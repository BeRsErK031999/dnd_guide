from uuid import UUID

from adapters.repository.sql.models.base import Base
from adapters.repository.sql.models.mixin import Timestamp
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Subrace(Timestamp, Base):
    __tablename__ = "subrace"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(100))
    increase_modifiers: Mapped[list["SubraceIncreaseModifier"]] = relationship(
        back_populates="race"
    )
    features: Mapped[list["SubraceFeature"]] = relationship(back_populates="race")


class SubraceIncreaseModifier(Timestamp, Base):
    __tablename__ = "subrace_increase_modifier"

    name: Mapped[str] = mapped_column(String(100))
    bonus: Mapped[int]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped["Subrace"] = relationship(back_populates="increase_modifiers")


class SubraceFeature(Timestamp, Base):
    __tablename__ = "subrace_feature"

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped["Subrace"] = relationship(back_populates="features")
