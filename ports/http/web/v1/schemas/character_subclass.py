from dataclasses import dataclass
from uuid import UUID

from domain.character_subclass import CharacterSubclass


@dataclass
class ReadSubclassSchema:
    subclass_id: UUID
    name: str
    description: str
    name_in_english: str

    @staticmethod
    def from_domain(subclass: CharacterSubclass) -> ReadSubclassSchema:
        return ReadSubclassSchema(
            subclass_id=subclass.subclass_id(),
            name=subclass.name(),
            description=subclass.description(),
            name_in_english=subclass.name_in_english(),
        )


@dataclass
class CreateSubclassSchema:
    name: str
    description: str
    name_in_english: str


@dataclass
class UpdateSubclassSchema:
    name: str | None
    description: str | None
    name_in_english: str | None
