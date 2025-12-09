from dataclasses import dataclass
from uuid import UUID

__all__ = ["SourceQuery", "SourcesQuery"]


@dataclass
class SourceQuery:
    source_id: UUID


@dataclass
class SourcesQuery:
    search_by_name: str | None = None
