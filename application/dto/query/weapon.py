from dataclasses import dataclass
from uuid import UUID


@dataclass
class WeaponQuery:
    weapon_id: UUID
