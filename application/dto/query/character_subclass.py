from dataclasses import dataclass
from uuid import UUID

__all__ = ["SubclassQuery", "SubclassesQuery"]


@dataclass
class SubclassQuery:
    subclass_id: UUID


@dataclass
class SubclassesQuery:
    filter_by_class_id: UUID | None = None
