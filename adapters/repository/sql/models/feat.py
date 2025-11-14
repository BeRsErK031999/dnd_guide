from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FeatModel(Base):
    __tablename__ = "feat"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    is_caster: Mapped[bool]

    increase_modifiers: Mapped[list[FeatIncreaseModifierModel]] = relationship(
        back_populates="feat"
    )
    required_modifiers: Mapped[list[FeatRequiredModifierModel]] = relationship(
        back_populates="feat"
    )
    required_armor_types: Mapped[list[FeatRequiredArmorTypeModel]] = relationship(
        back_populates="feat"
    )


class FeatIncreaseModifierModel(Base):
    __tablename__ = "feat_increase_modifier"

    name: Mapped[str] = mapped_column(String(50))
    feat_id: Mapped[UUID] = mapped_column(ForeignKey("feat.id"))

    feat: Mapped[FeatModel] = relationship(back_populates="increase_modifiers")


class FeatRequiredModifierModel(Base):
    __tablename__ = "feat_required_modifier"

    name: Mapped[str] = mapped_column(String(50))
    min_value: Mapped[int]
    feat_id: Mapped[UUID] = mapped_column(ForeignKey("feat.id"))

    feat: Mapped[FeatModel] = relationship(back_populates="required_modifiers")


class FeatRequiredArmorTypeModel(Base):
    __tablename__ = "feat_required_armor_type"

    name: Mapped[str] = mapped_column(String(50))
    feat_id: Mapped[UUID] = mapped_column(ForeignKey("feat.id"))

    feat: Mapped[FeatModel] = relationship(back_populates="required_armor_types")
