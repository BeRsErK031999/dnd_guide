from enum import IntEnum

from domain.error import DomainError


class Dice(IntEnum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D100 = 100

    @staticmethod
    def from_str(name: str) -> Dice:
        match name.upper():
            case Dice.D4.name:
                return Dice.D4
            case Dice.D6.name:
                return Dice.D6
            case Dice.D8.name:
                return Dice.D8
            case Dice.D10.name:
                return Dice.D10
            case Dice.D12.name:
                return Dice.D12
            case Dice.D20.name:
                return Dice.D20
            case Dice.D100.name:
                return Dice.D100
            case _:
                raise DomainError.invalid_data(
                    f"для кости с названием {name} не удалось сопоставить значение"
                )
