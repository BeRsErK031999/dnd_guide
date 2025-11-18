from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubraceQuery:
    subrace_id: UUID


@dataclass
class SubracesQuery:
    search_by_name: str | None = None
