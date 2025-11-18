from dataclasses import dataclass
from uuid import UUID


@dataclass
class SourceQuery:
    source_id: UUID


@dataclass
class SourcesQuery:
    search_by_name: str | None = None
