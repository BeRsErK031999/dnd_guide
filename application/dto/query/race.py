from dataclasses import dataclass
from uuid import UUID


@dataclass
class RaceQuery:
    race_id: UUID
