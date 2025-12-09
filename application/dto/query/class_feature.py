from dataclasses import dataclass
from uuid import UUID

__all__ = ["ClassFeatureQuery", "ClassFeaturesQuery"]


@dataclass
class ClassFeatureQuery:
    feature_id: UUID


@dataclass
class ClassFeaturesQuery:
    filter_by_class_id: UUID | None = None
