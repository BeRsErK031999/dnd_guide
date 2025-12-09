from dataclasses import dataclass
from uuid import UUID

__all__ = ["MaterialComponentQuery", "MaterialComponentsQuery"]


@dataclass
class MaterialComponentQuery:
    material_id: UUID


@dataclass
class MaterialComponentsQuery:
    search_by_name: str | None = None
