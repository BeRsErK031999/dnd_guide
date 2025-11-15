from dataclasses import dataclass
from uuid import UUID


@dataclass
class ClassLevelQuery:
    class_level_id: UUID
