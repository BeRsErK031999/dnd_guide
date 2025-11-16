from enum import IntEnum

from domain.error import DomainError


class DiceType(IntEnum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D100 = 100

    @staticmethod
    def from_str(name: str) -> "DiceType":
        match name.upper():
            case DiceType.D4.name:
                return DiceType.D4
            case DiceType.D6.name:
                return DiceType.D6
            case DiceType.D8.name:
                return DiceType.D8
            case DiceType.D10.name:
                return DiceType.D10
            case DiceType.D12.name:
                return DiceType.D12
            case DiceType.D20.name:
                return DiceType.D20
            case DiceType.D100.name:
                return DiceType.D100
            case _:
                raise DomainError.invalid_data(
                    f"для кости с названием {name} не удалось сопоставить значение"
                )


class Dice:
    def __init__(self, count: int, dice_type: DiceType) -> None:
        if count < 1:
            raise DomainError.invalid_data("количество костей не может быть меньше 1")
        self.__count = count
        self.__dice_type = dice_type

    def count(self) -> int:
        return self.__count

    def dice_type(self) -> DiceType:
        return self.__dice_type

    def __str__(self) -> str:
        return f"{self.__count}{self.__dice_type.name.lower()}"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.__count == value.__count and self.__dice_type == value.__dice_type
            )
        raise NotImplemented
