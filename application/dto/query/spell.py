from dataclasses import dataclass
from uuid import UUID


@dataclass
class SpellQuery:
    spell_id: UUID
