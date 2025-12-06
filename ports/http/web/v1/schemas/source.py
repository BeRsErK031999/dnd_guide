from dataclasses import dataclass
from uuid import UUID

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


@dataclass
class UpdateSourceSchema:
    name: str | None = None
    description: str | None = None
    name_in_english: str | None = None
