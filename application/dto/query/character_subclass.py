from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubclassQuery:
    subclass_id: UUID
