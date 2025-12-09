from dataclasses import dataclass
from uuid import UUID

__all__ = ["SubraceQuery", "SubracesQuery"]


@dataclass
class SubraceQuery:
    subrace_id: UUID


@dataclass
class SubracesQuery:
    search_by_name: str | None = None
