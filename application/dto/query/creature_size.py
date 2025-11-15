from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreatureSizeQuery:
    size_id: UUID
