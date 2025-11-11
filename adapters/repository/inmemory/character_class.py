from uuid import UUID, uuid4

from application.repository import ClassRepository as AppClassRepository
from domain.character_class import CharacterClass
from domain.character_class import ClassRepository as DomainClassRepository


class InMemoryClassRepository(DomainClassRepository, AppClassRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, CharacterClass] = {}

    async def name_exists(self, name: str) -> bool:
        return any(
            character_class.name() == name for character_class in self.__store.values()
        )

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, class_id: UUID) -> bool:
        return class_id in self.__store

    async def get_by_id(self, class_id: UUID) -> CharacterClass:
        return self.__store[class_id]

    async def get_all(self) -> list[CharacterClass]:
        return list(self.__store.values())

    async def create(self, character_class: CharacterClass) -> None:
        self.__store[character_class.class_id()] = character_class

    async def update(self, character_class: CharacterClass) -> None:
        self.__store[character_class.class_id()] = character_class

    async def delete(self, class_id: UUID) -> None:
        del self.__store[class_id]
