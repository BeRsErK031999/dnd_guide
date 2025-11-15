from typing import TYPE_CHECKING
from uuid import UUID

from adapters.repository.sql.models.base import Base
from domain.armor.armor_type import ArmorType
from domain.character_class import CharacterClass, ClassHits, ClassProficiencies
from domain.dice import Dice, DiceType
from domain.modifier import Modifier
from domain.skill import Skill
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

    primary_modifiers: Mapped[list[ClassPrimaryModifierModel]] = relationship(
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
    weapons: Mapped[list[WeaponModel]] = relationship(
        back_populates="character_classes", secondary="rel_class_weapon"
    )
    tools: Mapped[list[ToolModel]] = relationship(
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
    source: Mapped[SourceModel] = relationship(back_populates="character_classes")

    def to_domain(self) -> CharacterClass:
        hits = ClassHits(
            hit_dice=Dice(
                count=self.hit_dice_count,
                dice_type=DiceType.from_str(self.hit_dice_name),
            ),
            starting_hits=self.starting_hits,
            hit_modifier=Modifier.from_str(self.hit_modifier),
            next_level_hits=self.next_level_hits,
        )
        proficiencies = ClassProficiencies(
            armors=[armor_type.to_domain() for armor_type in self.armor_types],
            weapons=[weapon.id for weapon in self.weapons],
            tools=[tool.id for tool in self.tools],
            saving_throws=[
                saving_throw.to_domain() for saving_throw in self.saving_throws
            ],
            skills=[skill.to_domain() for skill in self.skills],
            number_skills=self.number_skills,
            number_tools=self.number_tools,
        )
        return CharacterClass(
            class_id=self.id,
            name=self.name,
            description=self.description,
            primary_modifiers=[m.to_domain() for m in self.primary_modifiers],
            hits=hits,
            proficiencies=proficiencies,
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )

    @staticmethod
    def from_domain(character_class: CharacterClass) -> CharacterClassModel:
        hits = character_class.hits()
        prof = character_class.proficiency()
        return CharacterClassModel(
            id=character_class.class_id(),
            name=character_class.name(),
            description=character_class.description(),
            name_in_english=character_class.name_in_english(),
            hit_dice_name=hits.dice().dice_type().name,
            hit_dice_count=hits.dice().count(),
            starting_hits=hits.starting(),
            hit_modifier=hits.modifier().name,
            next_level_hits=hits.standard_next_level(),
            number_skills=prof.number_skills(),
            number_tools=prof.number_tools(),
            source_id=character_class.source_id(),
        )


class ClassPrimaryModifierModel(Base):
    __tablename__ = "class_primary_modifier"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))

    character_class: Mapped[CharacterClassModel] = relationship(
        back_populates="primary_modifiers"
    )

    def to_domain(self) -> Modifier:
        return Modifier.from_str(self.name)

    @staticmethod
    def from_domain(class_id: UUID, modifier: Modifier) -> ClassPrimaryModifierModel:
        return ClassPrimaryModifierModel(name=modifier.name, class_id=class_id)


class ClassArmorTypeModel(Base):
    __tablename__ = "class_armor_type"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))

    character_class: Mapped[CharacterClassModel] = relationship(
        back_populates="armor_types"
    )

    def to_domain(self) -> ArmorType:
        return ArmorType.from_str(self.name)

    @staticmethod
    def from_domain(class_id: UUID, armor_type: ArmorType) -> ClassArmorTypeModel:
        return ClassArmorTypeModel(name=armor_type.name, class_id=class_id)


class ClassSavingThrowModel(Base):
    __tablename__ = "class_saving_throw"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))

    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="saving_throws"
    )

    def to_domain(self) -> Modifier:
        return Modifier.from_str(self.name)

    @staticmethod
    def from_domain(class_id: UUID, modifier: Modifier) -> ClassSavingThrowModel:
        return ClassSavingThrowModel(name=modifier.name, class_id=class_id)


class ClassSkillModel(Base):
    __tablename__ = "class_skill"

    name: Mapped[str] = mapped_column(String(50))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))

    character_class: Mapped["CharacterClassModel"] = relationship(
        back_populates="skills"
    )

    def to_domain(self) -> Skill:
        return Skill.from_str(self.name)

    @staticmethod
    def from_domain(class_id: UUID, skill: Skill) -> ClassSkillModel:
        return ClassSkillModel(name=skill.name, class_id=class_id)


class RelClassToolModel(Base):
    __tablename__ = "rel_class_tool"

    tool_id: Mapped[UUID] = mapped_column(ForeignKey("tool.id"))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))


class RelClassWeaponModel(Base):
    __tablename__ = "rel_class_weapon"

    weapon_id: Mapped[UUID] = mapped_column(ForeignKey("weapon.id"))
    class_id: Mapped[UUID] = mapped_column(ForeignKey("character_class.id"))
