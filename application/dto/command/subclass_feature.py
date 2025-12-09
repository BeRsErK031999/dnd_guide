from dataclasses import dataclass
from uuid import UUID

from domain.error import DomainError

__all__ = [
    "CreateSubclassFeatureCommand",
    "UpdateSubclassFeatureCommand",
    "DeleteSubclassFeatureCommand",
]


@dataclass
class CreateSubclassFeatureCommand:
    user_id: UUID
    subclass_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str


@dataclass
class UpdateSubclassFeatureCommand:
    user_id: UUID
    feature_id: UUID
    subclass_id: UUID | None
    name: str | None
    description: str | None
    level: int | None
    name_in_english: str | None

    def __post_init__(self) -> None:
        if all(
            [
                self.subclass_id is None,
                self.name is None,
                self.description is None,
                self.level is None,
                self.name_in_english is None,
            ]
        ):
            raise DomainError.invalid_data(
                "не переданы данные для обновления умения класса"
            )


@dataclass
class DeleteSubclassFeatureCommand:
    user_id: UUID
    feature_id: UUID
