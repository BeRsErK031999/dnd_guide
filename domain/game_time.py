from enum import StrEnum

from domain.error import DomainError


class GameTimeUnit(StrEnum):
    ACTION = "действие"
    BONUS_ACTION = "бонусное действие"
    REACTION = "реакция"
    MINUTE = "минута"
    HOUR = "час"

    @staticmethod
    def from_str(name: str) -> GameTimeUnit:
        match name.upper():
            case GameTimeUnit.ACTION.name:
                return GameTimeUnit.ACTION
            case GameTimeUnit.BONUS_ACTION.name:
                return GameTimeUnit.BONUS_ACTION
            case GameTimeUnit.REACTION.name:
                return GameTimeUnit.REACTION
            case GameTimeUnit.MINUTE.name:
                return GameTimeUnit.MINUTE
            case GameTimeUnit.HOUR.name:
                return GameTimeUnit.HOUR
            case _:
                raise DomainError.invalid_data(
                    f"для временного промежутка с названием {name} не "
                    "удалось сопоставить значение"
                )


class GameTime:
    def __init__(self, count: int, units: GameTimeUnit) -> None:
        if count < 0:
            raise DomainError.invalid_data(
                "отрицательного количества времени не может быть"
            )
        self.__count = count
        self.__units = units

    def count(self) -> int:
        return self.__count

    def units(self) -> GameTimeUnit:
        return self.__units

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__count == value.__count and self.__units == value.__units
        raise NotImplemented
