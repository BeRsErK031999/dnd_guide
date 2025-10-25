from domain.damage_type import DamageType
from domain.dice import Dice


class WeaponDamage:
    def __init__(
        self, dice: Dice, damage_type: DamageType, bonus_damage: int = 0
    ) -> None:
        self.__dice = dice
        self.__damage_type = damage_type
        self.__bonus_damage = bonus_damage

    def dice(self) -> Dice:
        return self.__dice

    def damage_type(self) -> DamageType:
        return self.__damage_type

    def bonus_damage(self) -> int:
        return self.__bonus_damage

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__dice == value.__dice
                and self.__damage_type == value.__damage_type
                and self.__bonus_damage == value.__bonus_damage
            )
        raise NotImplemented
