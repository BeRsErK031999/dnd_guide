from enum import StrEnum

from domain.error import DomainError


class ClassName(StrEnum):
    BARD = "бард"
    BARBARIAN = "варвар"
    FIGHTER = "воин"
    WIZARD = "волшебник"
    DRUID = "друид"
    CLERIC = "жрец"
    WARLOCK = "колдун"
    MONK = "монах"
    PALADIN = "паладин"
    ROGUE = "плут"
    RANGER = "следопыт"
    SORCERER = "чародей"

    @classmethod
    def from_str(cls, name: str) -> ClassName:
        match name:
            case ClassName.BARD.value:
                return ClassName.BARD
            case ClassName.BARBARIAN.value:
                return ClassName.BARBARIAN
            case ClassName.FIGHTER.value:
                return ClassName.FIGHTER
            case ClassName.WIZARD.value:
                return ClassName.WIZARD
            case ClassName.CLERIC.value:
                return ClassName.CLERIC
            case ClassName.WARLOCK.value:
                return ClassName.WARLOCK
            case ClassName.MONK.value:
                return ClassName.MONK
            case ClassName.PALADIN.value:
                return ClassName.PALADIN
            case ClassName.ROGUE.value:
                return ClassName.ROGUE
            case ClassName.RANGER.value:
                return ClassName.RANGER
            case ClassName.SORCERER.value:
                return ClassName.SORCERER
            case _:
                raise DomainError.invalid_data(
                    f"класса с названием {name} не существует"
                )
