from dataclasses import dataclass
from uuid import UUID


@dataclass
class ClassFeatureQuery:
    feature_id: UUID


@dataclass
class ClassFeaturesQuery:
    filter_by_class_id: UUID | None = None
