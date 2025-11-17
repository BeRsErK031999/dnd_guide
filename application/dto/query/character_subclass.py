from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubclassQuery:
    subclass_id: UUID


@dataclass
class SubclassesQuery:
    filter_by_class_id: UUID | None = None
