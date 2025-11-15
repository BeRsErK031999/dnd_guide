from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.character_class import CharacterClass, ClassHits, ClassProficiencies
from litestar.dto import DataclassDTO
from ports.http.web.schemas.dice import DiceSchema


@dataclass
class ClassHitsSchema:
    hit_dice: DiceSchema
    starting_hits: int
    hit_modifier: str
    next_level_hits: int

    @staticmethod
    def from_domain(hits: ClassHits) -> ClassHitsSchema:
        return ClassHitsSchema(
            hit_dice=DiceSchema.from_domain(hits.dice()),
            starting_hits=hits.starting(),
            hit_modifier=hits.modifier().value,
            next_level_hits=hits.standard_next_level(),
        )


@dataclass
class ClassProficienciesSchema:
    armors: Sequence[str]
    weapons: Sequence[UUID]
    tools: Sequence[UUID]
    saving_throws: Sequence[str]
    skills: Sequence[str]
    number_skills: int
    number_tools: int

    @staticmethod
    def from_domain(proficiencies: ClassProficiencies) -> ClassProficienciesSchema:
        return ClassProficienciesSchema(
            armors=proficiencies.armors(),
            weapons=proficiencies.weapons(),
            tools=proficiencies.tools(),
            saving_throws=proficiencies.saving_throws(),
            skills=proficiencies.skills(),
            number_skills=proficiencies.number_skills(),
            number_tools=proficiencies.number_tools(),
        )


@dataclass
class ReadClassSchema:
    class_id: UUID
    name: str
    description: str
    primary_modifiers: Sequence[str]
    hits: ClassHitsSchema
    proficiencies: ClassProficienciesSchema
    name_in_english: str
    source_id: UUID

    @staticmethod
    def from_domain(character_class: CharacterClass) -> ReadClassSchema:
        return ReadClassSchema(
            class_id=character_class.class_id(),
            name=character_class.name(),
            description=character_class.description(),
            primary_modifiers=character_class.primary_modifiers(),
            hits=ClassHitsSchema.from_domain(character_class.hits()),
            proficiencies=ClassProficienciesSchema.from_domain(
                character_class.proficiency()
            ),
            name_in_english=character_class.name_in_english(),
            source_id=character_class.source_id(),
        )


@dataclass
class CreateClassSchema:
    name: str
    description: str
    primary_modifiers: Sequence[str]
    hits: ClassHitsSchema
    proficiencies: ClassProficienciesSchema
    name_in_english: str
    source_id: UUID


class CreateClassDTO(DataclassDTO[CreateClassSchema]):
    pass


@dataclass
class UpdateClassSchema:
    name: str | None = None
    description: str | None = None
    primary_modifiers: Sequence[str] | None = None
    hits: ClassHitsSchema | None = None
    proficiencies: ClassProficienciesSchema | None = None
    name_in_english: str | None = None
    source_id: UUID | None = None


class UpdateClassDTO(DataclassDTO[UpdateClassSchema]):
    pass
