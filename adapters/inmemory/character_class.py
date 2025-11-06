from uuid import UUID, uuid4

from application.repository import ClassRepository as AppClassRepository
from domain.character_class import CharacterClass
from domain.character_class import ClassRepository as DomainClassRepository


class InMemoryClassRepository(DomainClassRepository, AppClassRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, CharacterClass] = {}

    async def is_name_exist(self, name: str) -> bool:
        return any(
            character_class.name == name for character_class in self.__store.values()
        )

    async def next_id(self) -> UUID:
        return uuid4()

    async def is_class_of_id_exist(self, class_id: UUID) -> bool:
        return class_id in self.__store

    async def get_class_of_id(self, class_id: UUID) -> CharacterClass:
        return self.__store[class_id]

    async def save(self, character_class: CharacterClass) -> None:
        self.__store[character_class.class_id()] = character_class

    async def delete(self, class_id: UUID) -> None:
        del self.__store[class_id]
