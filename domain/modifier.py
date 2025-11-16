from enum import StrEnum

from domain.error import DomainError


class Modifier(StrEnum):
    STRENGTH = "сила"
    DEXTERITY = "ловкость"
    CONSTITUTION = "телосложение"
    INTELLECT = "интеллект"
    WISDOM = "мудрость"
    CHARISMA = "харизма"

    @staticmethod
    def from_str(name: str) -> "Modifier":
        match name.upper():
            case Modifier.STRENGTH.name:
                return Modifier.STRENGTH
            case Modifier.DEXTERITY.name:
                return Modifier.DEXTERITY
            case Modifier.CONSTITUTION.name:
                return Modifier.CONSTITUTION
            case Modifier.INTELLECT.name:
                return Modifier.INTELLECT
            case Modifier.WISDOM.name:
                return Modifier.WISDOM
            case Modifier.CHARISMA.name:
                return Modifier.CHARISMA
            case _:
                raise DomainError.invalid_data(
                    f"для модификатора с названием {name} не удалось сопоставить значение"
                )
