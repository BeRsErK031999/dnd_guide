from dataclasses import dataclass
from uuid import UUID

from domain.subclass_feature import SubclassFeature


@dataclass
class ReadSubclassFeatureSchema:
    feature_id: UUID
    subclass_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str

    @staticmethod
    def from_domain(feature: SubclassFeature) -> ReadSubclassFeatureSchema:
        return ReadSubclassFeatureSchema(
            feature_id=feature.feature_id(),
            subclass_id=feature.subclass_id(),
            name=feature.name(),
            description=feature.description(),
            level=feature.level(),
            name_in_english=feature.name_in_english(),
        )


@dataclass
class CreateSubclassFeatureSchema:
    subclass_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str


@dataclass
class UpdateSubclassFeatureSchema:
    subclass_id: UUID | None
    name: str | None
    description: str | None
    level: int | None
    name_in_english: str | None
