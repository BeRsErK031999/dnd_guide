from dataclasses import dataclass
from uuid import UUID


@dataclass
class ClassLevelQuery:
    class_level_id: UUID


@dataclass
class ClassLevelsQuery:
    filter_by_class_id: UUID | None = None
