from dataclasses import dataclass
from uuid import UUID

from application.dto.command.class_feature import (
    CreateClassFeatureCommand,
    UpdateClassFeatureCommand,
)
from application.dto.model.class_feature import AppClassFeature


@dataclass
class ReadClassFeatureSchema:
    feature_id: UUID
    class_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str

    @staticmethod
    def from_app(feature: AppClassFeature) -> "ReadClassFeatureSchema":
        return ReadClassFeatureSchema(
            feature_id=feature.feature_id,
            class_id=feature.class_id,
            name=feature.name,
            description=feature.description,
            level=feature.level,
            name_in_english=feature.name_in_english,
        )


@dataclass
class CreateClassFeatureSchema:
    class_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str

    def to_command(self, user_id: UUID) -> CreateClassFeatureCommand:
        return CreateClassFeatureCommand(
            user_id=user_id,
            class_id=self.class_id,
            name=self.name,
            description=self.description,
            level=self.level,
            name_in_english=self.name_in_english,
        )


@dataclass
class UpdateClassFeatureSchema:
    class_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    level: int | None = None
    name_in_english: str | None = None

    def to_command(self, user_id: UUID, feature_id: UUID) -> UpdateClassFeatureCommand:
        return UpdateClassFeatureCommand(
            user_id=user_id,
            feature_id=feature_id,
            class_id=self.class_id,
            name=self.name,
            description=self.description,
            level=self.level,
            name_in_english=self.name_in_english,
        )
