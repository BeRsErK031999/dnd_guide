from dataclasses import dataclass
from uuid import UUID


@dataclass
class ClassQuery:
    class_id: UUID
