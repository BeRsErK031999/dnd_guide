from domain.dice import Dice
from domain.mixin import ValueDescription


class ClassLevelDice(ValueDescription):
    def __init__(
        self,
        dice: Dice,
        dice_description: str,
        number_dices: int = 1,
    ) -> None:
        ValueDescription.__init__(self, dice_description)
        self.__dice = dice
        self.__number_dices = number_dices

    def dice(self) -> Dice:
        return self.__dice

    def number_dices(self) -> int:
        return self.__number_dices

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__dice == value.__dice
                and self.__description == value.__description
                and self.__number_dices == value.__number_dices
            )
        raise NotImplemented
