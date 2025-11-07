from typing import Dict
from uuid import UUID, uuid4

from application.repository import SubclassRepository as AppSubclassRepository
from domain.character_subclass import CharacterSubclass
from domain.character_subclass import SubclassRepository as DomainSubclassRepository


class InMemorySubclassRepository(DomainSubclassRepository, AppSubclassRepository):
    def __init__(self) -> None:
        self.__store: Dict[UUID, CharacterSubclass] = {}

    async def is_name_exist(self, name: str) -> bool:
        return any(armor.name == name for armor in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def is_subclass_of_id_exist(self, subclass_id: UUID) -> bool:
        return subclass_id in self.__store

    async def get_subclass_of_id(self, subclass_id: UUID) -> CharacterSubclass:
        return self.__store[subclass_id]

    async def save(self, subclass: CharacterSubclass) -> None:
        self.__store[subclass.subclass_id()] = subclass

    async def delete(self, subclass_id: UUID) -> None:
        del self.__store[subclass_id]
