from dataclasses import dataclass
from uuid import UUID


@dataclass
class MaterialQuery:
    material_id: UUID


@dataclass
class MaterialsQuery:
    name: str | None = None
