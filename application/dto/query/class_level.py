from dataclasses import dataclass
from uuid import UUID

__all__ = ["ClassLevelQuery", "ClassLevelsQuery"]


@dataclass
class ClassLevelQuery:
    class_level_id: UUID


@dataclass
class ClassLevelsQuery:
    filter_by_class_id: UUID | None = None
