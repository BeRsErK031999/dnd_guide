from dataclasses import dataclass
from uuid import UUID

__all__ = ["ClassQuery", "ClassesQuery"]


@dataclass
class ClassQuery:
    class_id: UUID


@dataclass
class ClassesQuery:
    search_by_name: str | None = None
