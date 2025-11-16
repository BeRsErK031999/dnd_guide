from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.subrace import Subrace, SubraceFeature, SubraceIncreaseModifier


@dataclass
class SubraceFeatureSchema:
    name: str
    description: str

    @staticmethod
    def from_domain(feature: SubraceFeature) -> SubraceFeatureSchema:
        return SubraceFeatureSchema(
            name=feature.name(),
            description=feature.description(),
        )


@dataclass
class SubraceIncreaseModifierSchema:
    modifier: str
    bonus: int

    @staticmethod
    def from_domain(modifier: SubraceIncreaseModifier) -> SubraceIncreaseModifierSchema:
        return SubraceIncreaseModifierSchema(
            modifier=modifier.modifier().value,
            bonus=modifier.bonus(),
        )


@dataclass
class ReadSubraceSchema:
    subrace_id: UUID
    race_id: UUID
    name: str
    description: str
    increase_modifiers: Sequence[SubraceIncreaseModifierSchema]
    name_in_english: str
    features: Sequence[SubraceFeatureSchema]

    @staticmethod
    def from_domain(subrace: Subrace) -> ReadSubraceSchema:
        return ReadSubraceSchema(
            subrace_id=subrace.subrace_id(),
            race_id=subrace.race_id(),
            name=subrace.name(),
            description=subrace.description(),
            increase_modifiers=[
                SubraceIncreaseModifierSchema.from_domain(modifier)
                for modifier in subrace.increase_modifiers()
            ],
            name_in_english=subrace.name_in_english(),
            features=[
                SubraceFeatureSchema.from_domain(feature)
                for feature in subrace.features()
            ],
        )


@dataclass
class CreateSubraceSchema:
    race_id: UUID
    name: str
    description: str
    increase_modifiers: Sequence[SubraceIncreaseModifierSchema]
    name_in_english: str
    features: Sequence[SubraceFeatureSchema]


@dataclass
class UpdateSubraceSchema:
    race_id: UUID
    name: str | None = None
    description: str | None = None
    increase_modifiers: Sequence[SubraceIncreaseModifierSchema] | None = None
    new_features: Sequence[SubraceFeatureSchema] | None = None
    add_features: Sequence[SubraceFeatureSchema] | None = None
    remove_features: Sequence[str] | None = None
    name_in_english: str | None = None
