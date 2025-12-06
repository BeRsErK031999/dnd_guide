from dataclasses import dataclass
from uuid import UUID

from application.dto.command.character_subclass import (
    CreateSubclassCommand,
    UpdateSubclassCommand,
)
from application.dto.model.character_subclass import AppSubclass


@dataclass
class ReadSubclassSchema:
    subclass_id: UUID
    class_id: UUID
    name: str
    description: str
    name_in_english: str

    @staticmethod
    def from_app(subclass: AppSubclass) -> "ReadSubclassSchema":
        return ReadSubclassSchema(
            subclass_id=subclass.subclass_id,
            class_id=subclass.class_id,
            name=subclass.name,
            description=subclass.description,
            name_in_english=subclass.name_in_english,
        )


@dataclass
class CreateSubclassSchema:
    class_id: UUID
    name: str
    description: str
    name_in_english: str

    def to_command(self, user_id: UUID) -> CreateSubclassCommand:
        return CreateSubclassCommand(
            user_id=user_id,
            class_id=self.class_id,
            name=self.name,
            description=self.description,
            name_in_english=self.name_in_english,
        )


@dataclass
class UpdateSubclassSchema:
    class_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    name_in_english: str | None = None

    def to_command(self, user_id: UUID, subclass_id: UUID) -> UpdateSubclassCommand:
        return UpdateSubclassCommand(
            user_id=user_id,
            subclass_id=subclass_id,
            class_id=self.class_id,
            name=self.name,
            description=self.description,
            name_in_english=self.name_in_english,
        )
