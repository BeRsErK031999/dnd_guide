from dataclasses import dataclass
from uuid import UUID

__all__ = ["SubclassFeatureQuery", "SubclassFeaturesQuery"]


@dataclass
class SubclassFeatureQuery:
    feature_id: UUID


@dataclass
class SubclassFeaturesQuery:
    filter_by_subclass_id: UUID | None = None
