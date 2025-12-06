from dataclasses import dataclass
from uuid import UUID

from application.dto.command.source import CreateSourceCommand, UpdateSourceCommand
from application.dto.model.source import AppSource


@dataclass
class ReadSourceSchema:
    source_id: UUID
    name: str
    description: str
    name_in_english: str

    @staticmethod
    def from_app(source: AppSource) -> "ReadSourceSchema":
        return ReadSourceSchema(
            source_id=source.source_id,
            name=source.name,
            description=source.description,
            name_in_english=source.name_in_english,
        )


@dataclass
class CreateSourceSchema:
    name: str
    description: str
    name_in_english: str

    def to_command(self, user_id: UUID) -> CreateSourceCommand:
        return CreateSourceCommand(
            user_id=user_id,
            name=self.name,
            description=self.description,
            name_in_english=self.name_in_english,
        )


@dataclass
class UpdateSourceSchema:
    name: str | None = None
    description: str | None = None
    name_in_english: str | None = None

    def to_command(self, user_id: UUID, source_id: UUID) -> UpdateSourceCommand:
        return UpdateSourceCommand(
            user_id=user_id,
            source_id=source_id,
            name=self.name,
            description=self.description,
            name_in_english=self.name_in_english,
        )
