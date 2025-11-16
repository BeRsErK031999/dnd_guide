from dataclasses import dataclass
from uuid import UUID

from domain.dice import Dice
from domain.length import Length
from domain.weapon_property import WeaponProperty, WeaponPropertyName
from litestar.dto import DataclassDTO
from ports.http.web.v1.schemas.dice import DiceSchema
from ports.http.web.v1.schemas.length import LengthSchema


@dataclass
class ReadWeaponPropertyNameSchema:
    ammunition: str
    finesse: str
    heavy: str
    light: str
    reach: str
    special: str
    thrown: str
    two_handed: str
    versatile: str
    distance: str

    @staticmethod
    def from_domain() -> ReadWeaponPropertyNameSchema:
        return ReadWeaponPropertyNameSchema(
            **{name.name.lower(): name.value for name in WeaponPropertyName}
        )


@dataclass
class WeaponPropertyBaseRangeSchema:
    range: LengthSchema | None

    @staticmethod
    def from_domain(range: Length) -> WeaponPropertyBaseRangeSchema:
        return WeaponPropertyBaseRangeSchema(range=LengthSchema.from_domain(range))


@dataclass
class WeaponPropertyMaxRangeSchema:
    range: LengthSchema | None

    @staticmethod
    def from_domain(range: Length) -> WeaponPropertyMaxRangeSchema:
        return WeaponPropertyMaxRangeSchema(range=LengthSchema.from_domain(range))


@dataclass
class WeaponPropertySecondHandDiceSchema:
    dice: DiceSchema | None

    @staticmethod
    def from_domain(dice: Dice) -> WeaponPropertySecondHandDiceSchema:
        return WeaponPropertySecondHandDiceSchema(dice=DiceSchema.from_domain(dice))


@dataclass
class ReadWeaponPropertySchema:
    weapon_property_id: UUID
    name: str
    description: str
    base_range: WeaponPropertyBaseRangeSchema | None = None
    max_range: WeaponPropertyMaxRangeSchema | None = None
    second_hand_dice: WeaponPropertySecondHandDiceSchema | None = None

    @staticmethod
    def from_domain(weapon_property: WeaponProperty) -> ReadWeaponPropertySchema:
        base_range = weapon_property.base_range()
        max_range = weapon_property.max_range()
        second_hand_dice = weapon_property.second_hand_dice()
        return ReadWeaponPropertySchema(
            weapon_property_id=weapon_property.weapon_property_id(),
            name=weapon_property.name(),
            description=weapon_property.description(),
            base_range=(
                WeaponPropertyBaseRangeSchema.from_domain(base_range)
                if base_range is not None
                else None
            ),
            max_range=(
                WeaponPropertyMaxRangeSchema.from_domain(max_range)
                if max_range is not None
                else None
            ),
            second_hand_dice=(
                WeaponPropertySecondHandDiceSchema.from_domain(second_hand_dice)
                if second_hand_dice is not None
                else None
            ),
        )


@dataclass
class CreateWeaponPropertySchema:
    name: str
    description: str
    base_range: WeaponPropertyBaseRangeSchema | None = None
    max_range: WeaponPropertyMaxRangeSchema | None = None
    second_hand_dice: WeaponPropertySecondHandDiceSchema | None = None


class CreateWeaponPropertyDTO(DataclassDTO[CreateWeaponPropertySchema]):
    pass


@dataclass
class UpdateWeaponPropertySchema:
    name: str | None = None
    description: str | None = None
    base_range: WeaponPropertyBaseRangeSchema | None = None
    max_range: WeaponPropertyMaxRangeSchema | None = None
    second_hand_dice: WeaponPropertySecondHandDiceSchema | None = None


class UpdateWeaponPropertyDTO(DataclassDTO[UpdateWeaponPropertySchema]):
    pass
