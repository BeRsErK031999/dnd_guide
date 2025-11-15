from dataclasses import dataclass
from uuid import UUID


@dataclass
class WeaponPropertyQuery:
    weapon_property_id: UUID
