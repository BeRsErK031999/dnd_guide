from enum import StrEnum

from domain.error import DomainError


class LengthUnit(StrEnum):
    FT = "фут"
    M = "метр"


class Length:
    def __init__(self, count: float, unit: LengthUnit) -> None:
        if count < 0:
            raise DomainError.invalid_data("мера длины не может быть отрицательной")
        match unit:
            case LengthUnit.FT:
                self.__count = count
            case LengthUnit.M:
                self.__count = count * 3.281
            case _:
                raise DomainError.invalid_data("неизвестная единица длины")

    def in_ft(self) -> float:
        return self.__count

    def in_m(self) -> float:
        return self.__count / 3.281

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__count == value.__count
        raise NotImplemented

    def __lt__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__count < value.__count
        raise NotImplemented
