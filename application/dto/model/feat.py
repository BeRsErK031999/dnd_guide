from dataclasses import dataclass
from typing import Sequence
from uuid import UUID

from domain.armor.armor_type import ArmorType
from domain.feat import Feat, FeatRequiredModifier
from domain.modifier import Modifier


@dataclass
class AppFeatRequiredModifier:
    modifier: str
    min_value: int

    @staticmethod
    def from_domain(modifier: FeatRequiredModifier) -> "AppFeatRequiredModifier":
        return AppFeatRequiredModifier(
            modifier=modifier.modifier().value, min_value=modifier.min_value()
        )

    def to_domain(self) -> FeatRequiredModifier:
        return FeatRequiredModifier(
            modifier=Modifier.from_str(self.modifier),
            min_value=self.min_value,
        )


@dataclass
class AppFeat:
    feat_id: UUID
    name: str
    description: str
    caster: bool
    required_armor_types: Sequence[str]
    required_modifiers: Sequence[AppFeatRequiredModifier]
    increase_modifiers: Sequence[str]

    @staticmethod
    def from_domain(feat: Feat) -> "AppFeat":
        return AppFeat(
            feat_id=feat.feat_id(),
            name=feat.name(),
            description=feat.description(),
            caster=feat.caster(),
            required_armor_types=[
                armor_type.value for armor_type in feat.required_armor_types()
            ],
            required_modifiers=[
                AppFeatRequiredModifier.from_domain(modifier)
                for modifier in feat.required_modifiers()
            ],
            increase_modifiers=[
                modifier.value for modifier in feat.increase_modifiers()
            ],
        )

    def to_domain(self) -> Feat:
        return Feat(
            feat_id=self.feat_id,
            name=self.name,
            description=self.description,
            caster=self.caster,
            required_modifiers=[m.to_domain() for m in self.required_modifiers],
            required_armor_types=[
                ArmorType.from_str(t) for t in self.required_armor_types
            ],
            increase_modifiers=[Modifier.from_str(m) for m in self.increase_modifiers],
        )
