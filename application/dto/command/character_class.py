from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.error import DomainError


@dataclass
class ClassHitsCommand:
    hit_dice: str
    starting_hits: int
    hit_modifier: str
    next_level_hits: int


@dataclass
class ClassProficienciesCommand:
    armors: Sequence[str]
    weapon: Sequence[UUID]
    tools: Sequence[UUID]
    saving_throws: Sequence[str]
    skills: Sequence[str]
    number_skills: int
    number_tools: int = 1


@dataclass
class CreateClassCommand:
    user_id: UUID
    name: str
    description: str
    primary_modifiers: Sequence[str]
    hits: ClassHitsCommand
    proficiencies: ClassProficienciesCommand
    name_in_english: str = ""


@dataclass
class UpdateClassCommand:
    user_id: UUID
    class_id: UUID
    name: str | None = None
    description: str | None = None
    primary_modifiers: Sequence[str] | None = None
    hits: ClassHitsCommand | None = None
    proficiencies: ClassProficienciesCommand | None = None
    name_in_english: str | None = None

    def __post_init__(self) -> None:
        if all(
            [
                self.name is None,
                self.description is None,
                self.primary_modifiers is None,
                self.hits is None,
                self.proficiencies is None,
                self.name_in_english is None,
            ]
        ):
            raise DomainError.invalid_data("не переданы данные для обновления класса")


@dataclass
class DeleteClassCommand:
    user_id: UUID
    class_id: UUID
