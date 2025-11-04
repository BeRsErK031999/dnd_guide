from dataclasses import dataclass
from uuid import UUID

from domain.error import DomainError


@dataclass
class CreateCreatureSizeCommand:
    user_id: UUID
    name: str
    description: str


@dataclass
class UpdateCreatureSizeCommand:
    user_id: UUID
    size_id: UUID
    name: str | None
    description: str | None

    def __post_init__(self) -> None:
        if all([self.name is None, self.description is None]):
            raise DomainError.invalid_data(
                "не переданы данные для обновления размера существа"
            )


@dataclass
class DeleteCreatureSizeCommand:
    user_id: UUID
    size_id: UUID
