from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from application.dto.model.character_class import (
    AppClass,
    AppClassHits,
    AppClassProficiencies,
)
from application.dto.model.dice import AppDice
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from adapters.repository.sql.models.character_subclass import CharacterSubclassModel
    from adapters.repository.sql.models.class_feature import ClassFeatureModel
    from adapters.repository.sql.models.class_level import ClassLevelModel
    from adapters.repository.sql.models.source import SourceModel
    from adapters.repository.sql.models.spell import SpellModel
    from adapters.repository.sql.models.tool import ToolModel
    from adapters.repository.sql.models.weapon import WeaponModel


class CharacterClassModel(Base):
    __tablename__ = "character_class"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    name_in_english: Mapped[str] = mapped_column(String(50))
    hit_dice_name: Mapped[str] = mapped_column(String(50))
    hit_dice_count: Mapped[int]
    starting_hits: Mapped[int]
    hit_modifier: Mapped[str]
    next_level_hits: Mapped[int]
    number_skills: Mapped[int]
    number_tools: Mapped[int]
    source_id: Mapped[UUID] = mapped_column(ForeignKey("source.id"))

    primary_modifiers: Mapped[list["ClassPrimaryModifierModel"]] = relationship(
        back_populates="character_class", cascade="all, delete-orphan"
    )
    armor_types: Mapped[list["ClassArmorTypeModel"]] = relationship(
        back_populates="character_class", cascade="all, delete-orphan"
    )
    saving_throws: Mapped[list["ClassSavingThrowModel"]] = relationship(
        back_populates="character_class", cascade="all, delete-orphan"
    )
    skills: Mapped[list["ClassSkillModel"]] = relationship(
        back_populates="character_class", cascade="all, delete-orphan"
    )
    weapons: Mapped[list["WeaponModel"]] = relationship(
        back_populates="character_classes", secondary="rel_class_weapon"
    )
    tools: Mapped[list["ToolModel"]] = relationship(
        back_populates="character_classes", secondary="rel_class_tool"
    )
    features: Mapped[list["ClassFeatureModel"]] = relationship(
        back_populates="character_class", cascade="all, delete-orphan"
    )
    character_subclasses: Mapped[list["CharacterSubclassModel"]] = relationship(
        back_populates="character_class", cascade="all, delete-orphan"
    )
    class_levels: Mapped[list["ClassLevelModel"]] = relationship(
        back_populates="character_class", cascade="all, delete-orphan"
    )
    spells: Mapped[list["SpellModel"]] = relationship(
        back_populates="character_classes", secondary="rel_spell_character_class"
    )
    source: Mapped["SourceModel"] = relationship(back_populates="character_classes")

    def to_app(self) -> AppClass:
        return AppClass(
            class_id=self.id,
            name=self.name,
            description=self.description,
            primary_modifiers=[m.to_app() for m in self.primary_modifiers],
            hits=AppClassHits(
                hit_dice=AppDice(
                    count=self.hit_dice_count, dice_type=self.hit_dice_name
                ),
                starting_hits=self.starting_hits,
                hit_modifier=self.hit_modifier,
                next_level_hits=self.next_level_hits,
            ),
            proficiencies=AppClassProficiencies(
                armors=[a.to_app() for a in self.armor_types],
                weapons=[w.id for w in self.weapons],
                tools=[t.id for t in self.tools],
                saving_throws=[m.to_app() for m in self.saving_throws],
                skills=[s.to_app() for s in self.skills],
                number_skills=self.number_skills,
                number_tools=self.number_tools,
            ),
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )

    @staticmethod
    def from_app(app_class: AppClass) -> "CharacterClassModel":
        return CharacterClassModel(
            id=app_class.class_id,
            name=app_class.name,
            description=app_class.description,
            name_in_english=app_class.name_in_english,
            hit_dice_name=app_class.hits.hit_dice.dice_type,
            hit_dice_count=app_class.hits.hit_dice.count,
            starting_hits=app_class.hits.starting_hits,
            hit_modifier=app_class.hits.hit_modifier,
            next_level_hits=app_class.hits.next_level_hits,
            number_skills=app_class.proficiencies.number_skills,
            number_tools=app_class.proficiencies.number_tools,
            source_id=app_class.source_id,
        )


class ClassPrimaryModifierModel(Base):
    __tablename__ = "class_primary_modifier"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_class.id", ondelete="CASCADE")
    )

    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="primary_modifiers"
    )

    def to_app(self) -> str:
        return self.name

    @staticmethod
    def from_app(class_id: UUID, name: str) -> "ClassPrimaryModifierModel":
        return ClassPrimaryModifierModel(
            name=name,
            class_id=class_id,
        )


class ClassArmorTypeModel(Base):
    __tablename__ = "class_armor_type"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_class.id", ondelete="CASCADE")
    )

    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="armor_types"
    )

    def to_app(self) -> str:
        return self.name

    @staticmethod
    def from_app(class_id: UUID, name: str) -> "ClassArmorTypeModel":
        return ClassArmorTypeModel(
            name=name,
            class_id=class_id,
        )


class ClassSavingThrowModel(Base):
    __tablename__ = "class_saving_throw"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_class.id", ondelete="CASCADE")
    )

    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="saving_throws"
    )

    def to_app(self) -> str:
        return self.name

    @staticmethod
    def from_app(class_id: UUID, name: str) -> "ClassSavingThrowModel":
        return ClassSavingThrowModel(
            name=name,
            class_id=class_id,
        )


class ClassSkillModel(Base):
    __tablename__ = "class_skill"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_class.id", ondelete="CASCADE")
    )

    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="skills"
    )

    def to_app(self) -> str:
        return self.name

    @staticmethod
    def from_app(class_id: UUID, name: str) -> "ClassSkillModel":
        return ClassSkillModel(
            name=name,
            class_id=class_id,
        )


class RelClassToolModel(Base):
    __tablename__ = "rel_class_tool"

    tool_id: Mapped[UUID] = mapped_column(ForeignKey("tool.id", ondelete="CASCADE"))
    class_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_class.id", ondelete="CASCADE")
    )


class RelClassWeaponModel(Base):
    __tablename__ = "rel_class_weapon"

    weapon_id: Mapped[UUID] = mapped_column(ForeignKey("weapon.id", ondelete="CASCADE"))
    class_id: Mapped[UUID] = mapped_column(
        ForeignKey("character_class.id", ondelete="CASCADE")
    )
