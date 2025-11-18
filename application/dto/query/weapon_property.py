from dataclasses import dataclass
from uuid import UUID


@dataclass
class WeaponPropertyQuery:
    weapon_property_id: UUID


@dataclass
class WeaponPropertiesQuery:
    search_by_name: str | None = None
