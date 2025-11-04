from dataclasses import dataclass
from uuid import UUID

from domain.error import DomainError


@dataclass
class CreateCreatureTypeCommand:
    user_id: UUID
    name: str
    description: str


@dataclass
class UpdateCreatureTypeCommand:
    user_id: UUID
    type_id: UUID
    name: str | None
    description: str | None

    def __post_init__(self) -> None:
        if all([self.name is None, self.description is None]):
            raise DomainError.invalid_data(
                "не переданы данные для обновления типа существа"
            )


@dataclass
class DeleteCreatureTypeCommand:
    user_id: UUID
    type_id: UUID
