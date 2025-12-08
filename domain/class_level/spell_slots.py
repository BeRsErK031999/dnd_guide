from typing import Sequence

from domain.error import DomainError


class ClassLevelSpellSlots:
    def __init__(self, spell_slots: Sequence[int]) -> None:
        len_spells = len(spell_slots)
        if not (len_spells == 5 or len_spells == 9):
            raise DomainError.invalid_data(
                "количество ячеек заклинаний должно быть равно 5 или 9"
            )
        self._spell_slots = list(spell_slots)

    def slots(self) -> list[int]:
        return self._spell_slots

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._spell_slots == value._spell_slots
        raise NotImplemented
