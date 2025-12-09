from dataclasses import dataclass
from uuid import UUID

__all__ = ["RaceQuery", "RacesQuery"]


@dataclass
class RaceQuery:
    race_id: UUID


@dataclass
class RacesQuery:
    search_by_name: str | None = None
