from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_subclass import CharacterSubclass
    from adapters.repository.sql.models.class_feature import ClassFeature
    from adapters.repository.sql.models.class_level import ClassLevel
    from adapters.repository.sql.models.source import Source
    from adapters.repository.sql.models.spell import Spell


class CharacterClass(Base):
    __tablename__ = "character_class"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    starting_hits: Mapped[int]
    hit_modifier: Mapped[str]
    next_level_hits: Mapped[int]
    number_skills: Mapped[int]
    number_tools: Mapped[int]
    primary_modifiers: Mapped[list["ClassPrimaryModifier"]] = relationship(
        back_populates="character_class"
    )
    hit_dice: Mapped[list["ClassHitDice"]] = relationship(
        back_populates="character_class"
    )
    armor_types: Mapped[list["ClassArmorType"]] = relationship(
        back_populates="character_class"
    )
    saving_throws: Mapped[list["ClassSavingThrow"]] = relationship(
        back_populates="character_class"
    )
    skills: Mapped[list["ClassSkill"]] = relationship(back_populates="character_class")
    weapons: Mapped[list["RelClassWeapon"]] = relationship(
        back_populates="character_classes", secondary="rel_class_weapon"
    )
    tools: Mapped[list["RelClassTool"]] = relationship(
        back_populates="character_classes", secondary="rel_class_tool"
    )
    features: Mapped[list["ClassFeature"]] = relationship(
        back_populates="character_class"
    )
    character_subclasses: Mapped[list["CharacterSubclass"]] = relationship(
        back_populates="character_class"
    )
    class_levels: Mapped[list["ClassLevel"]] = relationship(
        back_populates="character_class"
    )
    spells: Mapped[list["Spell"]] = relationship(
        back_populates="character_classes", secondary="rel_spell_character_class"
    )
    source_id: Mapped[UUID] = mapped_column(ForeignKey("source.id"))
    source: Mapped["Source"] = relationship(back_populates="character_classes")


class ClassPrimaryModifier(Base):
    __tablename__ = "class_primary_modifier"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClass"] = relationship(
        back_populates="primary_modifiers"
    )


class ClassHitDice(Base):
    __tablename__ = "class_hit_dice"

    name: Mapped[str] = mapped_column(String(50))
    count: Mapped[int]
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClass"] = relationship(back_populates="hit_dice")


class ClassArmorType(Base):
    __tablename__ = "class_armor_type"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClass"] = relationship(
        back_populates="armor_types"
    )


class ClassSavingThrow(Base):
    __tablename__ = "class_saving_throw"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClass"] = relationship(
        back_populates="saving_throws"
    )


class ClassSkill(Base):
    __tablename__ = "class_skill"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
    character_class: Mapped["CharacterClass"] = relationship(back_populates="skills")


class RelClassTool(Base):
    __tablename__ = "rel_class_tool"

    tool_id: Mapped[UUID] = mapped_column(ForeignKey("tool.id"))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))


class RelClassWeapon(Base):
    __tablename__ = "rel_class_weapon"

    weapon_id: Mapped[UUID] = mapped_column(ForeignKey("weapon.id"))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
