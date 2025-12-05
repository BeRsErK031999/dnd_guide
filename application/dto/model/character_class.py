from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.armor.armor_type import ArmorType
from domain.character_class import CharacterClass, ClassHits, ClassProficiencies
from domain.modifier import Modifier
from domain.skill import Skill

from .dice import AppDice


@dataclass
class AppClassHits:
    hit_dice: AppDice
    starting_hits: int
    hit_modifier: str
    next_level_hits: int

    @staticmethod
    def from_domain(hits: ClassHits) -> "AppClassHits":
        return AppClassHits(
            hit_dice=AppDice.from_domain(hits.dice()),
            starting_hits=hits.starting(),
            hit_modifier=hits.modifier().value,
            next_level_hits=hits.standard_next_level(),
        )

    def to_domain(self) -> ClassHits:
        return ClassHits(
            hit_dice=self.hit_dice.to_domain(),
            starting_hits=self.starting_hits,
            hit_modifier=Modifier.from_str(self.hit_modifier),
            next_level_hits=self.next_level_hits,
        )


@dataclass
class AppClassProficiencies:
    armors: Sequence[str]
    weapons: Sequence[UUID]
    tools: Sequence[UUID]
    saving_throws: Sequence[str]
    skills: Sequence[str]
    number_skills: int
    number_tools: int

    @staticmethod
    def from_domain(proficiencies: ClassProficiencies) -> "AppClassProficiencies":
        return AppClassProficiencies(
            armors=proficiencies.armors(),
            weapons=proficiencies.weapons(),
            tools=proficiencies.tools(),
            saving_throws=proficiencies.saving_throws(),
            skills=proficiencies.skills(),
            number_skills=proficiencies.number_skills(),
            number_tools=proficiencies.number_tools(),
        )

    def to_domain(self) -> ClassProficiencies:
        return ClassProficiencies(
            armors=[ArmorType.from_str(a) for a in self.armors],
            weapons=self.weapons,
            tools=self.tools,
            saving_throws=[Modifier.from_str(t) for t in self.saving_throws],
            skills=[Skill.from_str(s) for s in self.skills],
            number_skills=self.number_skills,
            number_tools=self.number_tools,
        )


@dataclass
class AppClass:
    class_id: UUID
    name: str
    description: str
    primary_modifiers: Sequence[str]
    hits: AppClassHits
    proficiencies: AppClassProficiencies
    name_in_english: str
    source_id: UUID

    @staticmethod
    def from_domain(character_class: CharacterClass) -> "AppClass":
        return AppClass(
            class_id=character_class.class_id(),
            name=character_class.name(),
            description=character_class.description(),
            primary_modifiers=character_class.primary_modifiers(),
            hits=AppClassHits.from_domain(character_class.hits()),
            proficiencies=AppClassProficiencies.from_domain(
                character_class.proficiency()
            ),
            name_in_english=character_class.name_in_english(),
            source_id=character_class.source_id(),
        )

    def to_domain(self) -> CharacterClass:
        return CharacterClass(
            class_id=self.class_id,
            name=self.name,
            description=self.description,
            primary_modifiers=[Modifier.from_str(m) for m in self.primary_modifiers],
            hits=self.hits.to_domain(),
            proficiencies=self.proficiencies.to_domain(),
            name_in_english=self.name_in_english,
            source_id=self.source_id,
        )
