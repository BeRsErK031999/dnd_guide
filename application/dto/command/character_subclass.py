from dataclasses import dataclass
from uuid import UUID

from domain.error import DomainError


@dataclass
class CreateSubclassCommand:
    user_id: UUID
    class_id: UUID
    name: str
    description: str
    name_in_english: str


@dataclass
class UpdateSubclassCommand:
    user_id: UUID
    subclass_id: UUID
    class_id: UUID | None
    name: str | None
    description: str | None
    name_in_english: str | None

    def __post_init__(self) -> None:
        if all(
            [
                self.class_id is None,
                self.name is None,
                self.description is None,
                self.name_in_english is None,
            ]
        ):
            raise DomainError.invalid_data(
                "не переданы данные для обновления подкласса"
            )


@dataclass
class DeleteSubclassCommand:
    user_id: UUID
    subclass_id: UUID
