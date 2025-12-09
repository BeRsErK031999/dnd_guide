from dataclasses import dataclass
from uuid import UUID

from domain.armor import Armor, ArmorClass, ArmorType
from domain.modifier import Modifier

from .coin import AppCoins
from .weight import AppWeight

__all__ = ["AppArmorType", "AppArmorClass", "AppArmor"]


@dataclass
class AppArmorType:
    light_armor: str
    medium_armor: str
    heavy_armor: str
    shield: str

    @staticmethod
    def from_domain() -> "AppArmorType":
        return AppArmorType(
            **{armor_type.name.lower(): armor_type.value for armor_type in ArmorType}
        )


@dataclass
class AppArmorClass:
    base_class: int
    modifier: str | None
    max_modifier_bonus: int | None

    @staticmethod
    def from_domain(armor_class: ArmorClass) -> "AppArmorClass":
        modifier = armor_class.modifier()
        return AppArmorClass(
            base_class=armor_class.base_class(),
            modifier=modifier.value if modifier is not None else None,
            max_modifier_bonus=armor_class.max_modifier_bonus(),
        )

    def to_domain(self) -> ArmorClass:
        return ArmorClass(
            base_class=self.base_class,
            modifier=(
                Modifier.from_str(self.modifier) if self.modifier is not None else None
            ),
            max_modifier_bonus=self.max_modifier_bonus,
        )


@dataclass
class AppArmor:
    armor_id: UUID
    armor_type: str
    name: str
    description: str
    armor_class: AppArmorClass
    strength: int
    stealth: bool
    weight: AppWeight
    cost: AppCoins
    material_id: UUID

    @staticmethod
    def from_domain(armor: Armor) -> "AppArmor":
        return AppArmor(
            armor_id=armor.armor_id(),
            armor_type=armor.armor_type().value,
            name=armor.name(),
            description=armor.description(),
            armor_class=AppArmorClass.from_domain(armor.armor_class()),
            strength=armor.strength(),
            stealth=armor.stealth(),
            weight=AppWeight.from_domain(armor.weight()),
            cost=AppCoins.from_domain(armor.cost()),
            material_id=armor.material_id(),
        )

    def to_domain(self) -> Armor:
        return Armor(
            armor_id=self.armor_id,
            armor_type=ArmorType.from_str(self.armor_type),
            name=self.name,
            description=self.description,
            armor_class=self.armor_class.to_domain(),
            strength=self.strength,
            stealth=self.stealth,
            weight=self.weight.to_domain(),
            cost=self.cost.to_domain(),
            material_id=self.material_id,
        )
