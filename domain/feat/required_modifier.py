from domain.error import DomainError
from domain.modifier import Modifier


class FeatRequiredModifier:
    def __init__(self, modifier: Modifier, min_value: int) -> None:
        if min_value < 1 or min_value > 20:
            raise DomainError.invalid_data(
                "минимальное значение требуемых модификаторов должно находиться в "
                "диапазоне от 1 до 20"
            )
        self._modifier = modifier
        self._min_value = min_value

    def modifier(self) -> Modifier:
        return self._modifier

    def min_value(self) -> int:
        return self._min_value

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self._min_value == value._min_value
                and self._modifier == value._modifier
            )
        raise NotImplemented

    def __hash__(self) -> int:
        return hash((self._modifier, self._min_value))
