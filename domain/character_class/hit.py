from domain.dice import Dice
from domain.error import DomainError
from domain.modifier import Modifier


class ClassHits:
    def __init__(
        self,
        hit_dice: Dice,
        starting_hits: int,
        hit_modifier: Modifier,
        next_level_hits: int,
    ) -> None:
        if starting_hits < 1:
            raise DomainError.invalid_data(
                "количество начальных хитов не может быть меньше 1"
            )
        if next_level_hits < 1:
            raise DomainError.invalid_data(
                "количество хитов при увеличении уровня не может быть меньше 1"
            )
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

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__dice == value.__dice
                and self.__starting == value.__starting
                and self.__modifier == value.__modifier
                and self.__next_level == value.__next_level
            )
        raise NotImplemented
