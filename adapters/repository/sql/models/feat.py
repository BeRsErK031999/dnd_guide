from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.armor import ArmorType
from domain.feat import Feat, FeatRequiredModifier
from domain.modifier import Modifier
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class FeatModel(Base):
    __tablename__ = "feat"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    caster: Mapped[bool]

    increase_modifiers: Mapped[list["FeatIncreaseModifierModel"]] = relationship(
        back_populates="feat"
    )
    required_modifiers: Mapped[list["FeatRequiredModifierModel"]] = relationship(
        back_populates="feat"
    )
    required_armor_types: Mapped[list["FeatRequiredArmorTypeModel"]] = relationship(
        back_populates="feat"
    )

    def to_domain(self) -> Feat:
        return Feat(
            feat_id=self.id,
            name=self.name,
            description=self.description,
            caster=self.caster,
            increase_modifiers=[
                increase_modifier.to_domain()
                for increase_modifier in self.increase_modifiers
            ],
            required_modifiers=[
                required_modifier.to_domain()
                for required_modifier in self.required_modifiers
            ],
            required_armor_types=[
                required_armor_type.to_domain()
                for required_armor_type in self.required_armor_types
            ],
        )

    @staticmethod
    def from_domain(feat: Feat) -> "FeatModel":
        return FeatModel(
            name=feat.name(),
            description=feat.description(),
            caster=feat.caster(),
        )


class FeatIncreaseModifierModel(Base):
    __tablename__ = "feat_increase_modifier"

    name: Mapped[str] = mapped_column(String(50))
    feat_id: Mapped[UUID] = mapped_column(ForeignKey("feat.id"))

    feat: Mapped["FeatModel"] = relationship(back_populates="increase_modifiers")

    def to_domain(self) -> Modifier:
        return Modifier.from_str(self.name)

    @staticmethod
    def from_domain(feat_id: UUID, modifier: Modifier) -> "FeatIncreaseModifierModel":
        return FeatIncreaseModifierModel(name=modifier.name, feat_id=feat_id)


class FeatRequiredModifierModel(Base):
    __tablename__ = "feat_required_modifier"

    name: Mapped[str] = mapped_column(String(50))
    min_value: Mapped[int]
    feat_id: Mapped[UUID] = mapped_column(ForeignKey("feat.id"))

    feat: Mapped["FeatModel"] = relationship(back_populates="required_modifiers")

    def to_domain(self) -> FeatRequiredModifier:
        return FeatRequiredModifier(
            modifier=Modifier.from_str(self.name),
            min_value=self.min_value,
        )

    @staticmethod
    def from_domain(
        feat_id: UUID, required_modifier: FeatRequiredModifier
    ) -> "FeatRequiredModifierModel":
        return FeatRequiredModifierModel(
            name=required_modifier.modifier().name,
            min_value=required_modifier.min_value(),
            feat_id=feat_id,
        )


class FeatRequiredArmorTypeModel(Base):
    __tablename__ = "feat_required_armor_type"

    name: Mapped[str] = mapped_column(String(50))
    feat_id: Mapped[UUID] = mapped_column(ForeignKey("feat.id"))

    feat: Mapped["FeatModel"] = relationship(back_populates="required_armor_types")

    def to_domain(self) -> ArmorType:
        return ArmorType.from_str(self.name)

    @staticmethod
    def from_domain(
        feat_id: UUID, armor_type: ArmorType
    ) -> "FeatRequiredArmorTypeModel":
        return FeatRequiredArmorTypeModel(feat_id=feat_id, name=armor_type.name)
