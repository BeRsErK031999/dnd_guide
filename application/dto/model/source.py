from dataclasses import dataclass
from uuid import UUID

from domain.source import Source


@dataclass
class AppSource:
    source_id: UUID
    name: str
    description: str
    name_in_english: str

    @staticmethod
    def from_domain(source: Source) -> "AppSource":
        return AppSource(
            source_id=source.source_id(),
            name=source.name(),
            description=source.description(),
            name_in_english=source.name_in_english(),
        )

    def to_domain(self) -> Source:
        return Source(
            source_id=self.source_id,
            name=self.name,
            description=self.description,
            name_in_english=self.name_in_english,
        )
