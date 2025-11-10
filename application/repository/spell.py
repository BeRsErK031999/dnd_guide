from abc import ABC, abstractmethod
from uuid import UUID

from domain.spell import Spell


class SpellRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, spell_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, spell_id: UUID) -> Spell:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Spell]:
        raise NotImplemented

    @abstractmethod
    async def save(self, spell: Spell) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, spell_id: UUID) -> None:
        raise NotImplemented
