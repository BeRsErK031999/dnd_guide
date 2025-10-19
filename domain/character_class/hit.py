from domain.dice import Dice
from domain.modifier import Modifier


class ClassHit:
    def __init__(
        self,
        hit_dice: Dice,
        starting_hits: int,
        hit_modifier: Modifier,
        next_level_hits: int,
    ) -> None:
        self.__dice = hit_dice
        self.__starting = starting_hits
        self.__modifier = hit_modifier
        self.__next_level = next_level_hits

    def dice(self) -> Dice:
        return self.__dice

    def starting(self) -> int:
        return self.__starting

    def modifier(self) -> Modifier:
        return self.__modifier

    def random_next_level(self) -> Dice:
        return self.__dice

    def standard_next_level(self) -> int:
        return self.__next_level

    def __str__(self) -> str:
        return (
            f"кость: {self.__dice}, начальные хиты: {self.__starting}, "
            f"хиты на следующих уровнях {self.__dice} или {self.__next_level}, "
            f"модификатор: {self.__modifier}"
        )
