from abc import ABC, abstractmethod
from uuid import UUID

from domain.spell.spell import Spell


class SpellRepository(ABC):
    @abstractmethod
    def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_spell_of_id_exist(self, spell_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_spell_of_id(self, spell_id: UUID) -> Spell:
        raise NotImplemented

    @abstractmethod
    async def save(self, spell: Spell) -> None:
        raise NotImplemented
