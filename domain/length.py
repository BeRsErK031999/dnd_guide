from enum import StrEnum

from domain.error import DomainError


class LengthUnit(StrEnum):
    FT = "фут"
    M = "метр"

    @staticmethod
    def from_str(name: str) -> "LengthUnit":
        match name.upper():
            case LengthUnit.FT.name:
                return LengthUnit.FT
            case LengthUnit.M.name:
                return LengthUnit.M
            case _:
                raise DomainError.invalid_data(
                    f"для единиц {name} не удалось сопоставить значение"
                )


class Length:
    def __init__(self, count: float, unit: LengthUnit) -> None:
        if count < 0:
            raise DomainError.invalid_data("мера длины не может быть отрицательной")
        match unit:
            case LengthUnit.FT:
                self._count = count
            case LengthUnit.M:
                self._count = count * 3.281
            case _:
                raise DomainError.invalid_data("неизвестная единица длины")

    def in_ft(self) -> float:
        return self._count

    def in_m(self) -> float:
        return self._count / 3.281

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._count == value._count
        raise NotImplemented

    def __lt__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._count < value._count
        raise NotImplemented
