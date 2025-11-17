from enum import StrEnum

from domain.error import DomainError


class CreatureSize(StrEnum):
    TINY = "крошечный"
    SMALL = "малый"
    MEDIUM = "средний"
    LARGE = "большой"
    HUGE = "огромный"
    GARGANTUAN = "гигантский"

    @staticmethod
    def from_str(name: str) -> "CreatureSize":
        match name.upper():
            case CreatureSize.TINY.name:
                return CreatureSize.TINY
            case CreatureSize.SMALL.name:
                return CreatureSize.SMALL
            case CreatureSize.MEDIUM.name:
                return CreatureSize.MEDIUM
            case CreatureSize.LARGE.name:
                return CreatureSize.LARGE
            case CreatureSize.HUGE.name:
                return CreatureSize.HUGE
            case CreatureSize.GARGANTUAN.name:
                return CreatureSize.GARGANTUAN
            case _:
                raise DomainError.invalid_data(
                    f"для размера существа с названием {name} не удалось "
                    "сопоставить значение"
                )
