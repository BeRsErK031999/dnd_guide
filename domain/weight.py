from enum import StrEnum

from domain.error import DomainError


class WeightUnit(StrEnum):
    LB = "фунт"
    KG = "килограмм"


class Weight:
    def __init__(self, count: float, unit: WeightUnit) -> None:
        if count < 0:
            raise DomainError.invalid_data("масса не может быть отрицательной")
        match unit:
            case WeightUnit.LB:
                self.__count = count
            case WeightUnit.KG:
                self.__count = 2.205 * count
            case _:
                raise DomainError.invalid_data("неизвестная единица измерения массы")

    def in_lb(self) -> float:
        return self.__count

    def in_kg(self) -> float:
        return self.__count / 2.205

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__count == value.__count
        raise NotImplemented
