from domain.damage_type import DamageType
from domain.dice import Dice


class WeaponDamage:
    def __init__(
        self, dice: Dice, damage_type: DamageType, bonus_damage: int = 0
    ) -> None:
        self._dice = dice
        self._damage_type = damage_type
        self._bonus_damage = bonus_damage

    def dice(self) -> Dice:
        return self._dice

    def damage_type(self) -> DamageType:
        return self._damage_type

    def bonus_damage(self) -> int:
        return self._bonus_damage

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._dice == value._dice
                and self._damage_type == value._damage_type
                and self._bonus_damage == value._bonus_damage
            )
        raise NotImplemented
