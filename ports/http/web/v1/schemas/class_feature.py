from dataclasses import dataclass
from uuid import UUID

from domain.class_feature import ClassFeature
from litestar.dto import DataclassDTO


@dataclass
class ReadClassFeatureSchema:
    feature_id: UUID
    class_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str

    @staticmethod
    def from_domain(feature: ClassFeature) -> ReadClassFeatureSchema:
        return ReadClassFeatureSchema(
            feature_id=feature.feature_id(),
            class_id=feature.class_id(),
            name=feature.name(),
            description=feature.description(),
            level=feature.level(),
            name_in_english=feature.name_in_english(),
        )


@dataclass
class CreateClassFeatureSchema:
    class_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str


class CreateClassFeatureDTO(DataclassDTO[CreateClassFeatureSchema]):
    pass


@dataclass
class UpdateClassFeatureSchema:
    class_id: UUID | None
    name: str | None
    description: str | None
    level: int | None
    name_in_english: str | None


class UpdateClassFeatureDTO(DataclassDTO[UpdateClassFeatureSchema]):
    pass
