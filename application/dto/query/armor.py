from dataclasses import dataclass
from uuid import UUID


@dataclass
class ArmorQuery:
    armor_id: UUID


@dataclass
class ArmorsQuery:
    search_by_name: str | None = None
    filter_by_armor_types: list[str] | None = None
    filter_by_material_ids: list[UUID] | None = None
