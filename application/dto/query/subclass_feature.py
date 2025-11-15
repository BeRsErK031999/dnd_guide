from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubclassFeatureQuery:
    feature_id: UUID
