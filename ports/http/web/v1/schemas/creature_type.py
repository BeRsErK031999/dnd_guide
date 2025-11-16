from dataclasses import dataclass
from uuid import UUID

from domain.creature_type import CreatureType


@dataclass
class ReadCreatureTypeSchema:
    type_id: UUID
    name: str
    description: str

    @staticmethod
    def from_domain(type: CreatureType) -> "ReadCreatureTypeSchema":
        return ReadCreatureTypeSchema(
            type_id=type.type_id(),
            name=type.name(),
            description=type.description(),
        )


@dataclass
class CreateCreatureTypeSchema:
    name: str
    description: str


@dataclass
class UpdateCreatureTypeSchema:
    name: str | None = None
    description: str | None = None
