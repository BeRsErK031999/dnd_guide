from dataclasses import dataclass
from uuid import UUID

from domain.subclass_feature import SubclassFeature

__all__ = ["AppSubclassFeature"]


@dataclass
class AppSubclassFeature:
    feature_id: UUID
    subclass_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str

    @staticmethod
    def from_domain(feature: SubclassFeature) -> "AppSubclassFeature":
        return AppSubclassFeature(
            feature_id=feature.feature_id(),
            subclass_id=feature.subclass_id(),
            name=feature.name(),
            description=feature.description(),
            level=feature.level(),
            name_in_english=feature.name_in_english(),
        )

    def to_domain(self) -> SubclassFeature:
        return SubclassFeature(
            feature_id=self.feature_id,
            subclass_id=self.subclass_id,
            name=self.name,
            description=self.description,
            level=self.level,
            name_in_english=self.name_in_english,
        )
