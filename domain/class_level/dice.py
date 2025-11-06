from domain.dice import Dice
from domain.mixin import ValueDescription


class ClassLevelDice(ValueDescription):
    def __init__(
        self,
        dice: Dice,
        dice_description: str,
    ) -> None:
        ValueDescription.__init__(self, dice_description)
        self.__dice = dice

    def dice(self) -> Dice:
        return self.__dice

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__dice == value.__dice
                and self.__description == value.__description
            )
        raise NotImplemented
