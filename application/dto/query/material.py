from dataclasses import dataclass
from uuid import UUID

__all__ = ["MaterialQuery", "MaterialsQuery"]


@dataclass
class MaterialQuery:
    material_id: UUID


@dataclass
class MaterialsQuery:
    search_by_name: str | None = None
