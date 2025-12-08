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
        self._dice = hit_dice
        self._starting = starting_hits
        self._modifier = hit_modifier
        self._next_level = next_level_hits

    def dice(self) -> Dice:
        return self._dice

    def starting(self) -> int:
        return self._starting

    def modifier(self) -> Modifier:
        return self._modifier

    def random_next_level(self) -> Dice:
        return self._dice

    def standard_next_level(self) -> int:
        return self._next_level

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._dice == value._dice
                and self._starting == value._starting
                and self._modifier == value._modifier
                and self._next_level == value._next_level
            )
        raise NotImplemented
