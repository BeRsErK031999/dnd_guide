from dataclasses import dataclass
from uuid import UUID


@dataclass
class WeaponKindQuery:
    weapon_kind_id: UUID
