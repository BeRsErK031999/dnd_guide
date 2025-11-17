from dataclasses import dataclass
from uuid import UUID


@dataclass
class ClassQuery:
    class_id: UUID


@dataclass
class ClassesQuery:
    search_by_name: str | None = None
