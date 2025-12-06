from dataclasses import dataclass
from uuid import UUID

from application.dto.command.subclass_feature import (
    CreateSubclassFeatureCommand,
    UpdateSubclassFeatureCommand,
)
from application.dto.model.subclass_feature import AppSubclassFeature


@dataclass
class ReadSubclassFeatureSchema:
    feature_id: UUID
    subclass_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str

    @staticmethod
    def from_app(feature: AppSubclassFeature) -> "ReadSubclassFeatureSchema":
        return ReadSubclassFeatureSchema(
            feature_id=feature.feature_id,
            subclass_id=feature.subclass_id,
            name=feature.name,
            description=feature.description,
            level=feature.level,
            name_in_english=feature.name_in_english,
        )


@dataclass
class CreateSubclassFeatureSchema:
    subclass_id: UUID
    name: str
    description: str
    level: int
    name_in_english: str

    def to_command(self, user_id: UUID) -> CreateSubclassFeatureCommand:
        return CreateSubclassFeatureCommand(
            user_id=user_id,
            subclass_id=self.subclass_id,
            name=self.name,
            description=self.description,
            level=self.level,
            name_in_english=self.name_in_english,
        )


@dataclass
class UpdateSubclassFeatureSchema:
    subclass_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    level: int | None = None
    name_in_english: str | None = None

    def to_command(
        self, user_id: UUID, feature_id: UUID
    ) -> UpdateSubclassFeatureCommand:
        return UpdateSubclassFeatureCommand(
            user_id=user_id,
            feature_id=feature_id,
            subclass_id=self.subclass_id,
            name=self.name,
            description=self.description,
            level=self.level,
            name_in_english=self.name_in_english,
        )
