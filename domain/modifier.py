from enum import StrEnum

from domain.error import DomainError


class Modifier(StrEnum):
    STRENGTH = "сила"
    DEXTERITY = "ловкость"
    CONSTITUTION = "телосложение"
    INTELLIGENT = "интеллект"
    WISDOM = "мудрость"
    CHARISMA = "харизма"

    @staticmethod
    def from_str(name: str) -> Modifier:
        match name:
            case Modifier.STRENGTH.value:
                return Modifier.STRENGTH
            case Modifier.DEXTERITY.value:
                return Modifier.DEXTERITY
            case Modifier.CONSTITUTION.value:
                return Modifier.CONSTITUTION
            case Modifier.INTELLIGENT.value:
                return Modifier.INTELLIGENT
            case Modifier.WISDOM.value:
                return Modifier.WISDOM
            case Modifier.CHARISMA.value:
                return Modifier.CHARISMA
            case _:
                raise DomainError.invalid_data(
                    f"для модификатора с названием {name} не удалось сопоставить значение"
                )
