from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_subclass import CharacterSubclassModel
    from adapters.repository.sql.models.class_feature import ClassFeatureModel
    from adapters.repository.sql.models.class_level import ClassLevelModel
    from adapters.repository.sql.models.source import SourceModel
    from adapters.repository.sql.models.spell import SpellModel


class CharacterClassModel(Base):
    __tablename__ = "character_class"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    starting_hits: Mapped[int]
    hit_modifier: Mapped[str]
    next_level_hits: Mapped[int]
    number_skills: Mapped[int]
    number_tools: Mapped[int]
    primary_modifiers: Mapped[list[ClassPrimaryModifierModel]] = relationship(
        back_populates="character_class"
    )
    hit_dice: Mapped[list[ClassHitDiceModel]] = relationship(
        back_populates="character_class"
    )
    armor_types: Mapped[list[ClassArmorTypeModel]] = relationship(
        back_populates="character_class"
    )
    saving_throws: Mapped[list[ClassSavingThrowModel]] = relationship(
        back_populates="character_class"
    )
    skills: Mapped[list[ClassSkillModel]] = relationship(
        back_populates="character_class"
    )
    weapons: Mapped[list[RelClassWeaponModel]] = relationship(
        back_populates="character_classes", secondary="rel_class_weapon"
    )
    tools: Mapped[list[RelClassToolModel]] = relationship(
        back_populates="character_classes", secondary="rel_class_tool"
    )
    features: Mapped[list[ClassFeatureModel]] = relationship(
        back_populates="character_class"
    )
    character_subclasses: Mapped[list[CharacterSubclassModel]] = relationship(
        back_populates="character_class"
    )
    class_levels: Mapped[list[ClassLevelModel]] = relationship(
        back_populates="character_class"
    )
    spells: Mapped[list[SpellModel]] = relationship(
        back_populates="character_classes", secondary="rel_spell_character_class"
    )
    source_id: Mapped[UUID] = mapped_column(ForeignKey("source.id"))
    source: Mapped[SourceModel] = relationship(back_populates="character_classes")


class ClassPrimaryModifierModel(Base):
    __tablename__ = "class_primary_modifier"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="primary_modifiers"
    )


class ClassHitDiceModel(Base):
    __tablename__ = "class_hit_dice"

    name: Mapped[str] = mapped_column(String(50))
    count: Mapped[int]
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="hit_dice"
    )


class ClassArmorTypeModel(Base):
    __tablename__ = "class_armor_type"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="armor_types"
    )


class ClassSavingThrowModel(Base):
    __tablename__ = "class_saving_throw"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="saving_throws"
    )


class ClassSkillModel(Base):
    __tablename__ = "class_skill"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="skills"
    )


class RelClassToolModel(Base):
    __tablename__ = "rel_class_tool"

    tool_id: Mapped[UUID] = mapped_column(ForeignKey("tool.id"))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))


class RelClassWeaponModel(Base):
    __tablename__ = "rel_class_weapon"

    weapon_id: Mapped[UUID] = mapped_column(ForeignKey("weapon.id"))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
