from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.feat import AppFeat, AppFeatRequiredModifier
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FeatModel(Base):
    __tablename__ = "feat"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    caster: Mapped[bool]

    increase_modifiers: Mapped[list["FeatIncreaseModifierModel"]] = relationship(
        back_populates="feat", cascade="all, delete-orphan"
    )
    required_modifiers: Mapped[list["FeatRequiredModifierModel"]] = relationship(
        back_populates="feat", cascade="all, delete-orphan"
    )
    required_armor_types: Mapped[list["FeatRequiredArmorTypeModel"]] = relationship(
        back_populates="feat", cascade="all, delete-orphan"
    )

    def to_app(self) -> AppFeat:
        return AppFeat(
            feat_id=self.id,
            name=self.name,
            description=self.description,
            caster=self.caster,
            increase_modifiers=[m.to_app() for m in self.increase_modifiers],
            required_armor_types=[t.to_app() for t in self.required_armor_types],
            required_modifiers=[m.to_app() for m in self.required_modifiers],
        )

    @staticmethod
    def from_app(feat: AppFeat) -> "FeatModel":
        return FeatModel(
            id=feat.feat_id,
            name=feat.name,
            description=feat.description,
            caster=feat.caster,
        )


class FeatIncreaseModifierModel(Base):
    __tablename__ = "feat_increase_modifier"

    name: Mapped[str] = mapped_column(String(50))
    feat_id: Mapped[UUID] = mapped_column(ForeignKey("feat.id", ondelete="CASCADE"))

    feat: Mapped["FeatModel"] = relationship(back_populates="increase_modifiers")

    def to_app(self) -> str:
        return self.name

    @staticmethod
    def from_app(feat_id: UUID, name: str) -> "FeatIncreaseModifierModel":
        return FeatIncreaseModifierModel(name=name, feat_id=feat_id)


class FeatRequiredModifierModel(Base):
    __tablename__ = "feat_required_modifier"

    name: Mapped[str] = mapped_column(String(50))
    min_value: Mapped[int]
    feat_id: Mapped[UUID] = mapped_column(ForeignKey("feat.id", ondelete="CASCADE"))

    feat: Mapped["FeatModel"] = relationship(back_populates="required_modifiers")

    def to_app(self) -> AppFeatRequiredModifier:
        return AppFeatRequiredModifier(modifier=self.name, min_value=self.min_value)

    @staticmethod
    def from_app(
        feat_id: UUID, modifier: AppFeatRequiredModifier
    ) -> "FeatRequiredModifierModel":
        return FeatRequiredModifierModel(
            name=modifier.modifier, min_value=modifier.min_value, feat_id=feat_id
        )


class FeatRequiredArmorTypeModel(Base):
    __tablename__ = "feat_required_armor_type"

    name: Mapped[str] = mapped_column(String(50))
    feat_id: Mapped[UUID] = mapped_column(ForeignKey("feat.id", ondelete="CASCADE"))

    feat: Mapped["FeatModel"] = relationship(back_populates="required_armor_types")

    def to_app(self) -> str:
        return self.name

    @staticmethod
    def from_app(feat_id: UUID, name: str) -> "FeatRequiredArmorTypeModel":
        return FeatRequiredArmorTypeModel(name=name, feat_id=feat_id)
