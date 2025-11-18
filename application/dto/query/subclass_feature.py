from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubclassFeatureQuery:
    feature_id: UUID


@dataclass
class SubclassFeaturesQuery:
    filter_by_subclass_id: UUID | None = None
