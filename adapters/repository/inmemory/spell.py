from uuid import UUID, uuid4

from application.repository import SpellRepository as AppSpellRepository
from domain.spell import Spell
from domain.spell import SpellRepository as DomainSpellRepository


class InMemorySpellRepository(DomainSpellRepository, AppSpellRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, Spell] = {}

    async def name_exists(self, name: str) -> bool:
        return any(spell.name() == name for spell in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, spell_id: UUID) -> bool:
        return spell_id in self.__store

    async def get_by_id(self, spell_id: UUID) -> Spell:
        return self.__store[spell_id]

    async def save(self, spell: Spell) -> None:
        self.__store[spell.spell_id()] = spell

    async def delete(self, spell_id: UUID) -> None:
        del self.__store[spell_id]
