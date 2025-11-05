from enum import StrEnum

from domain.error import DomainError


class SpellSchool(StrEnum):
    ABJURATION = "ограждение"
    CONJURATION = "вызов"
    DIVINATION = "прорицание"
    ENCHANTMENT = "очарование"
    EVOCATION = "воплощение"
    ILLUSION = "иллюзия"
    NECROMANCY = "некромантия"
    TRANSMUTATION = "преобразование"

    @staticmethod
    def from_str(name: str) -> SpellSchool:
        match name.upper():
            case SpellSchool.ABJURATION.name:
                return SpellSchool.ABJURATION
            case SpellSchool.CONJURATION.name:
                return SpellSchool.CONJURATION
            case SpellSchool.DIVINATION.name:
                return SpellSchool.DIVINATION
            case SpellSchool.ENCHANTMENT.name:
                return SpellSchool.ENCHANTMENT
            case SpellSchool.EVOCATION.name:
                return SpellSchool.EVOCATION
            case SpellSchool.ILLUSION.name:
                return SpellSchool.ILLUSION
            case SpellSchool.NECROMANCY.name:
                return SpellSchool.NECROMANCY
            case SpellSchool.TRANSMUTATION.name:
                return SpellSchool.TRANSMUTATION
            case _:
                raise DomainError.invalid_data(f"неизвестная школа заклинаний: {name}")
