from dataclasses import dataclass
from uuid import UUID


@dataclass
class MaterialComponentQuery:
    material_id: UUID
