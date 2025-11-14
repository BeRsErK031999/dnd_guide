from dataclasses import dataclass
from uuid import UUID


@dataclass
class ArmorQuery:
    armor_id: UUID
