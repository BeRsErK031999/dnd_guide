from dataclasses import dataclass
from uuid import UUID

from domain.creature_size import CreatureSize
from litestar.dto import DataclassDTO


@dataclass
class ReadCreatureSizeSchema:
    size_id: UUID
    name: str
    description: str

    @staticmethod
    def from_domain(size: CreatureSize) -> ReadCreatureSizeSchema:
        return ReadCreatureSizeSchema(
            size_id=size.size_id(),
            name=size.name(),
            description=size.description(),
        )


@dataclass
class CreateCreatureSizeSchema:
    name: str
    description: str


class CreateCreatureSizeDTO(DataclassDTO[CreateCreatureSizeSchema]):
    pass


@dataclass
class UpdateCreatureSizeSchema:
    name: str | None
    description: str | None


class UpdateCreatureSizeDTO(DataclassDTO[UpdateCreatureSizeSchema]):
    pass
