from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreatureTypeQuery:
    type_id: UUID
