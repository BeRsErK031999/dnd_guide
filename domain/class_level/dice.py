from domain.dice import Dice
from domain.mixin import ValueDescription


class ClassLevelDice(ValueDescription):
    def __init__(
        self,
        dice: Dice,
        dice_description: str,
    ) -> None:
        ValueDescription.__init__(self, dice_description)
        self._dice = dice

    def dice(self) -> Dice:
        return self._dice

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._dice == value._dice and self._description == value._description
        raise NotImplemented
