from dataclasses import dataclass
from uuid import UUID

from domain.error import DomainError


@dataclass
class CreateSourceCommand:
    user_id: UUID
    name: str
    description: str
    name_in_english: str


@dataclass
class UpdateSourceCommand:
    user_id: UUID
    source_id: UUID
    name: str | None = None
    description: str | None = None
    name_in_english: str | None = None

    def __post_init__(self) -> None:
        if all(
            [self.name is None, self.description is None, self.name_in_english is None]
        ):
            raise DomainError.invalid_data(
                "не переданы данные для обновления источника"
            )


@dataclass
class DeleteSourceCommand:
    user_id: UUID
    source_id: UUID
