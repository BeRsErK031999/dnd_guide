from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from application.dto.command.subrace import (
    CreateSubraceCommand,
    SubraceFeatureCommand,
    SubraceIncreaseModifierCommand,
    UpdateSubraceCommand,
)
from application.dto.model.subrace import (
    AppSubrace,
    AppSubraceFeature,
    AppSubraceIncreaseModifier,
)


@dataclass
class SubraceFeatureSchema:
    name: str
    description: str

    @staticmethod
    def from_app(feature: AppSubraceFeature) -> "SubraceFeatureSchema":
        return SubraceFeatureSchema(name=feature.name, description=feature.description)

    def to_command(self) -> SubraceFeatureCommand:
        return SubraceFeatureCommand(name=self.name, description=self.description)


@dataclass
class SubraceIncreaseModifierSchema:
    modifier: str
    bonus: int

    @staticmethod
    def from_app(
        modifier: AppSubraceIncreaseModifier,
    ) -> "SubraceIncreaseModifierSchema":
        return SubraceIncreaseModifierSchema(
            modifier=modifier.modifier, bonus=modifier.bonus
        )

    def to_command(self) -> SubraceIncreaseModifierCommand:
        return SubraceIncreaseModifierCommand(modifier=self.modifier, bonus=self.bonus)


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
    def from_app(subrace: AppSubrace) -> "ReadSubraceSchema":
        return ReadSubraceSchema(
            subrace_id=subrace.subrace_id,
            race_id=subrace.race_id,
            name=subrace.name,
            description=subrace.description,
            increase_modifiers=[
                SubraceIncreaseModifierSchema.from_app(m)
                for m in subrace.increase_modifiers
            ],
            name_in_english=subrace.name_in_english,
            features=[SubraceFeatureSchema.from_app(f) for f in subrace.features],
        )


@dataclass
class CreateSubraceSchema:
    race_id: UUID
    name: str
    description: str
    increase_modifiers: Sequence[SubraceIncreaseModifierSchema]
    name_in_english: str
    features: Sequence[SubraceFeatureSchema]

    def to_command(self, user_id: UUID) -> CreateSubraceCommand:
        return CreateSubraceCommand(
            user_id=user_id,
            race_id=self.race_id,
            name=self.name,
            description=self.description,
            increase_modifiers=[m.to_command() for m in self.increase_modifiers],
            name_in_english=self.name_in_english,
            features=[f.to_command() for f in self.features],
        )


@dataclass
class UpdateSubraceSchema:
    race_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    increase_modifiers: Sequence[SubraceIncreaseModifierSchema] | None = None
    new_features: Sequence[SubraceFeatureSchema] | None = None
    add_features: Sequence[SubraceFeatureSchema] | None = None
    remove_features: Sequence[str] | None = None
    name_in_english: str | None = None

    def to_command(self, user_id: UUID, subrace_id: UUID) -> UpdateSubraceCommand:
        im = self.increase_modifiers
        if im is not None:
            im = [m.to_command() for m in im]
        nf = self.new_features
        if nf is not None:
            nf = [f.to_command() for f in nf]
        af = self.add_features
        if af is not None:
            af = [f.to_command() for f in af]
        return UpdateSubraceCommand(
            user_id=user_id,
            subrace_id=subrace_id,
            race_id=self.race_id,
            name=self.name,
            description=self.description,
            increase_modifiers=im,
            new_features=nf,
            add_features=af,
            remove_features=self.remove_features,
            name_in_english=self.name_in_english,
        )
