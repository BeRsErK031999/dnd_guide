from enum import StrEnum

from domain.error import DomainError


class PieceType(StrEnum):
    COPPER = "медные"
    SILVER = "серебряные"
    ELECTRUM = "электрум"
    GOLD = "золотые"
    PLATINUM = "платиновые"

    @staticmethod
    def from_str(name: str) -> PieceType:
        match name.upper():
            case PieceType.COPPER.name:
                return PieceType.COPPER
            case PieceType.SILVER.name:
                return PieceType.SILVER
            case PieceType.ELECTRUM.name:
                return PieceType.ELECTRUM
            case PieceType.GOLD.name:
                return PieceType.GOLD
            case PieceType.PLATINUM.name:
                return PieceType.PLATINUM
            case _:
                raise DomainError.invalid_data(
                    f"для типа монет с названием {name} не удалось сопоставить "
                    "значение"
                )


class Coins:
    def __init__(self, count: int, piece_type: PieceType = PieceType.COPPER) -> None:
        if count < 0:
            raise DomainError.invalid_data(
                "количество монет не может быть отрицательным"
            )
        match piece_type:
            case PieceType.COPPER:
                self.__count = count
            case PieceType.SILVER:
                self.__count = count * 10
            case PieceType.ELECTRUM:
                self.__count = count * 50
            case PieceType.GOLD:
                self.__count = count * 100
            case PieceType.PLATINUM:
                self.__count = count * 1000
            case _:
                raise DomainError.invalid_data("неизвестный тип монет")

    def in_copper(self) -> float:
        return self.__count

    def in_silver(self) -> float:
        return self.__count / 10

    def in_electrum(self) -> float:
        return self.__count / 50

    def in_gold(self) -> float:
        return self.__count / 100

    def in_platinum(self) -> float:
        return self.__count / 1_000

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__count == value.__count
        raise NotImplemented
