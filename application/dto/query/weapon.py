from dataclasses import dataclass
from uuid import UUID

__all__ = ["WeaponQuery", "WeaponsQuery"]


@dataclass
class WeaponQuery:
    weapon_id: UUID


@dataclass
class WeaponsQuery:
    search_by_name: str | None = None
    filter_by_kind_ids: list[UUID] | None = None
    filter_by_damage_types: list[str] | None = None
    filter_by_property_ids: list[UUID] | None = None
    filter_by_material_ids: list[UUID] | None = None
