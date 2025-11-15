from dataclasses import dataclass
from uuid import UUID


@dataclass
class ClassFeatureQuery:
    feature_id: UUID
