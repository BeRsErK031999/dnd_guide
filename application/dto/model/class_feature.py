from dataclasses import dataclass
from uuid import UUID

from domain.class_feature import ClassFeature


@dataclass
class AppClassFeature:
    feature_id: UUID
    class_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str

    @staticmethod
    def from_domain(feature: ClassFeature) -> "AppClassFeature":
        return AppClassFeature(
            feature_id=feature.feature_id(),
            class_id=feature.class_id(),
            name=feature.name(),
            description=feature.description(),
            level=feature.level(),
            name_in_english=feature.name_in_english(),
        )

    def to_domain(self) -> ClassFeature:
        return ClassFeature(
            feature_id=self.feature_id,
            class_id=self.class_id,
            name=self.name,
            description=self.description,
            level=self.level,
            name_in_english=self.name_in_english,
        )
