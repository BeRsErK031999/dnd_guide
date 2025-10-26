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
            case cls.BARD.value:
                return cls.BARD
            case cls.BARBARIAN.value:
                return cls.BARBARIAN
            case cls.FIGHTER.value:
                return cls.FIGHTER
            case cls.WIZARD.value:
                return cls.WIZARD
            case cls.CLERIC.value:
                return cls.CLERIC
            case cls.WARLOCK.value:
                return cls.WARLOCK
            case cls.MONK.value:
                return cls.MONK
            case cls.PALADIN.value:
                return cls.PALADIN
            case cls.ROGUE.value:
                return cls.ROGUE
            case cls.RANGER.value:
                return cls.RANGER
            case cls.SORCERER.value:
                return cls.SORCERER
            case _:
                raise DomainError.invalid_data(
                    f"класса с названием {name} не существует"
                )
