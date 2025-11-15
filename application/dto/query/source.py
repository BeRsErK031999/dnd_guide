from dataclasses import dataclass
from uuid import UUID


@dataclass
class SourceQuery:
    source_id: UUID
