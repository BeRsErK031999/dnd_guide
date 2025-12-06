from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.command.feat import (
    CreateFeatCommand,
    FeatRequiredModifierCommand,
    UpdateFeatCommand,
)
from application.dto.model.feat import AppFeat, AppFeatRequiredModifier


@dataclass
class FeatRequiredModifierSchema:
    modifier: str
    min_value: int

    @staticmethod
    def from_app(modifier: AppFeatRequiredModifier) -> "FeatRequiredModifierSchema":
        return FeatRequiredModifierSchema(
            modifier=modifier.modifier, min_value=modifier.min_value
        )

    def to_command(self) -> FeatRequiredModifierCommand:
        return FeatRequiredModifierCommand(
            modifier=self.modifier, min_value=self.min_value
        )


@dataclass
class ReadFeatSchema:
    feat_id: UUID
    name: str
    description: str
    caster: bool
    required_armor_types: Sequence[str]
    required_modifiers: Sequence[FeatRequiredModifierSchema]
    increase_modifiers: Sequence[str]

    @staticmethod
    def from_app(feat: AppFeat) -> "ReadFeatSchema":
        return ReadFeatSchema(
            feat_id=feat.feat_id,
            name=feat.name,
            description=feat.description,
            caster=feat.caster,
            required_armor_types=feat.required_armor_types,
            required_modifiers=[
                FeatRequiredModifierSchema.from_app(m) for m in feat.required_modifiers
            ],
            increase_modifiers=feat.increase_modifiers,
        )


@dataclass
class CreateFeatSchema:
    name: str
    description: str
    caster: bool
    required_armor_types: Sequence[str]
    required_modifiers: Sequence[FeatRequiredModifierSchema]
    increase_modifiers: Sequence[str]

    def to_command(self, user_id: UUID) -> CreateFeatCommand:
        return CreateFeatCommand(
            user_id=user_id,
            name=self.name,
            description=self.description,
            caster=self.caster,
            required_armor_types=self.required_armor_types,
            required_modifiers=[m.to_command() for m in self.required_modifiers],
            increase_modifiers=self.increase_modifiers,
        )


@dataclass
class UpdateFeatSchema:
    name: str | None = None
    description: str | None = None
    caster: bool | None = None
    required_armor_types: Sequence[str] | None = None
    required_modifiers: Sequence[FeatRequiredModifierSchema] | None = None
    increase_modifiers: Sequence[str] | None = None

    def to_command(self, user_id: UUID, feat_id: UUID) -> UpdateFeatCommand:
        rm = self.required_modifiers
        if rm is not None:
            rm = [m.to_command() for m in rm]
        return UpdateFeatCommand(
            user_id=user_id,
            feat_id=feat_id,
            name=self.name,
            description=self.description,
            caster=self.caster,
            required_armor_types=self.required_armor_types,
            required_modifiers=rm,
            increase_modifiers=self.increase_modifiers,
        )
