from domain.error import DomainError
from domain.modifier import Modifier


class RaceIncreaseModifier:
    def __init__(self, modifier: Modifier, bonus: int) -> None:
        if bonus < 1 or bonus > 5:
            raise DomainError.invalid_data(
                "бонус модификатора для расы должен находиться в диапазоне от 1 до 5"
            )
        self.__modifier = modifier
        self.__bonus = bonus

    def modifier(self) -> Modifier:
        return self.__modifier

    def bonus(self) -> int:
        return self.__bonus

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__modifier == value.__modifier and self.__bonus == value.__bonus
        raise NotImplemented
