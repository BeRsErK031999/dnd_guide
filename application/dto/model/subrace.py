from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.modifier import Modifier
from domain.subrace import Subrace, SubraceFeature, SubraceIncreaseModifier

__all__ = ["AppSubrace", "AppSubraceFeature", "AppSubraceIncreaseModifier"]


@dataclass
class AppSubraceFeature:
    name: str
    description: str

    @staticmethod
    def from_domain(feature: SubraceFeature) -> "AppSubraceFeature":
        return AppSubraceFeature(
            name=feature.name(),
            description=feature.description(),
        )

    def to_domain(self) -> SubraceFeature:
        return SubraceFeature(name=self.name, description=self.description)


@dataclass
class AppSubraceIncreaseModifier:
    modifier: str
    bonus: int

    @staticmethod
    def from_domain(
        modifier: SubraceIncreaseModifier,
    ) -> "AppSubraceIncreaseModifier":
        return AppSubraceIncreaseModifier(
            modifier=modifier.modifier().name.lower(),
            bonus=modifier.bonus(),
        )

    def to_domain(self) -> SubraceIncreaseModifier:
        return SubraceIncreaseModifier(
            modifier=Modifier.from_str(self.modifier), bonus=self.bonus
        )


@dataclass
class AppSubrace:
    subrace_id: UUID
    race_id: UUID
    name: str
    description: str
    increase_modifiers: Sequence[AppSubraceIncreaseModifier]
    name_in_english: str
    features: Sequence[AppSubraceFeature]

    @staticmethod
    def from_domain(subrace: Subrace) -> "AppSubrace":
        return AppSubrace(
            subrace_id=subrace.subrace_id(),
            race_id=subrace.race_id(),
            name=subrace.name(),
            description=subrace.description(),
            increase_modifiers=[
                AppSubraceIncreaseModifier.from_domain(modifier)
                for modifier in subrace.increase_modifiers()
            ],
            name_in_english=subrace.name_in_english(),
            features=[
                AppSubraceFeature.from_domain(feature) for feature in subrace.features()
            ],
        )

    def to_domain(self) -> Subrace:
        return Subrace(
            subrace_id=self.subrace_id,
            race_id=self.race_id,
            name=self.name,
            description=self.description,
            increase_modifiers=[m.to_domain() for m in self.increase_modifiers],
            features=[f.to_domain() for f in self.features],
            name_in_english=self.name_in_english,
        )
