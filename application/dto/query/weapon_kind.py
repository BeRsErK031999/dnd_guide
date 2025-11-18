from dataclasses import dataclass
from uuid import UUID


@dataclass
class WeaponKindQuery:
    weapon_kind_id: UUID


@dataclass
class WeaponKindsQuery:
    search_by_name: str | None = None
    filter_by_types: list[str] | None = None
