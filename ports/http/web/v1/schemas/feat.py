from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

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


@dataclass
class UpdateFeatSchema:
    name: str | None = None
    description: str | None = None
    caster: bool | None = None
    required_armor_types: Sequence[str] | None = None
    required_modifiers: Sequence[FeatRequiredModifierSchema] | None = None
    increase_modifiers: Sequence[str] | None = None
