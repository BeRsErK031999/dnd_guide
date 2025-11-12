from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class SubraceModel(Base):
    __tablename__ = "subrace"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    increase_modifiers: Mapped[list[SubraceIncreaseModifierModel]] = relationship(
        back_populates="race"
    )
    features: Mapped[list[SubraceFeatureModel]] = relationship(back_populates="race")


class SubraceIncreaseModifierModel(Base):
    __tablename__ = "subrace_increase_modifier"

    name: Mapped[str] = mapped_column(String(50))
    bonus: Mapped[int]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped[SubraceModel] = relationship(back_populates="increase_modifiers")


class SubraceFeatureModel(Base):
    __tablename__ = "subrace_feature"

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str]
    race_id: Mapped[UUID] = mapped_column(ForeignKey("race.id"))
    race: Mapped[SubraceModel] = relationship(back_populates="features")
