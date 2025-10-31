from typing import Sequence

from domain.error import DomainError


class SpellSlots:
    def __init__(self, spell_slots: Sequence[int]) -> None:
        len_spells = len(spell_slots)
        if len_spells < 5 or len_spells > 9:
            raise DomainError.invalid_data(
                "количество ячеек заклинаний должно находиться в диапазоне от 5 до 9"
            )
        self.__spell_slots = list(spell_slots)

    def slots(self) -> list[int]:
        return self.__spell_slots

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__spell_slots == value.__spell_slots
        raise NotImplemented
