from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubraceQuery:
    subrace_id: UUID
