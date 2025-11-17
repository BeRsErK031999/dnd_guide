from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.feat import Feat, FeatRequiredModifier


@dataclass
class FeatRequiredModifierSchema:
    modifier: str
    min_value: int

    @staticmethod
    def from_domain(modifier: FeatRequiredModifier) -> "FeatRequiredModifierSchema":
        return FeatRequiredModifierSchema(
            modifier=modifier.modifier().value, min_value=modifier.min_value()
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
    def from_domain(feat: Feat) -> "ReadFeatSchema":
        return ReadFeatSchema(
            feat_id=feat.feat_id(),
            name=feat.name(),
            description=feat.description(),
            caster=feat.caster(),
            required_armor_types=[
                armor_type.value for armor_type in feat.required_armor_types()
            ],
            required_modifiers=[
                FeatRequiredModifierSchema.from_domain(modifier)
                for modifier in feat.required_modifiers()
            ],
            increase_modifiers=[
                modifier.value for modifier in feat.increase_modifiers()
            ],
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
