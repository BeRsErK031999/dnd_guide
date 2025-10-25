from domain.error import DomainError
from domain.modifier import Modifier


class ArmorClass:
    def __init__(
        self,
        base_class: int,
        modifier: Modifier | None,
        max_modifier_bonus: int | None,
    ) -> None:
        if base_class < 1 or base_class > 20:
            raise DomainError.invalid_data(
                "базовый КД доспехов должен находиться в диапазоне от 1 до 20"
            )
        if max_modifier_bonus is not None and modifier is None:
            raise DomainError.invalid_data(
                "бонус от модификации нельзя указывать без указания модификации"
            )
        if max_modifier_bonus is not None and (
            max_modifier_bonus < 1 or max_modifier_bonus > 10
        ):
            raise DomainError.invalid_data(
                "бонус от модификации должен находиться в диапазоне от 1 до 10"
            )
        self.__base_class = base_class
        self.__modifier = modifier
        self.__max_modifier_bonus = max_modifier_bonus

    def base_class(self) -> int:
        return self.__base_class

    def modifier(self) -> Modifier | None:
        return self.__modifier

    def max_modifier_bonus(self) -> int | None:
        return self.__max_modifier_bonus

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__base_class == value.__base_class
                and self.__modifier == value.__modifier
                and self.__max_modifier_bonus == value.__max_modifier_bonus
            )
        raise NotImplemented
