from dataclasses import dataclass
from uuid import UUID

from domain.creature_size import CreatureSize


@dataclass
class ReadCreatureSizeSchema:
    size_id: UUID
    name: str
    description: str

    @staticmethod
    def from_domain(size: CreatureSize) -> "ReadCreatureSizeSchema":
        return ReadCreatureSizeSchema(
            size_id=size.size_id(),
            name=size.name(),
            description=size.description(),
        )


@dataclass
class CreateCreatureSizeSchema:
    name: str
    description: str


@dataclass
class UpdateCreatureSizeSchema:
    name: str | None = None
    description: str | None = None
