from dataclasses import dataclass
from uuid import UUID


@dataclass
class FeatQuery:
    feat_id: UUID
