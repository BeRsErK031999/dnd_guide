from uuid import UUID, uuid4

from application.repository import ClassLevelRepository as AppClassLevelRepository
from domain.class_level import ClassLevel
from domain.class_level import ClassLevelRepository as DomainClassLevelRepository


class InMemoryClassLevelRepository(DomainClassLevelRepository, AppClassLevelRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, ClassLevel] = {}

    async def level_of_class_exists(self, class_id: UUID, level: int) -> bool:
        return any(
            level == lvl.level()
            for lvl in self.__store.values()
            if lvl.class_id() == class_id
        )

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, level_id: UUID) -> bool:
        return level_id in self.__store

    async def get_by_id(self, level_id: UUID) -> ClassLevel:
        return self.__store[level_id]

    async def get_all(self) -> list[ClassLevel]:
        return list(self.__store.values())

    async def create(self, level: ClassLevel) -> None:
        self.__store[level.level_id()] = level

    async def update(self, level: ClassLevel) -> None:
        self.__store[level.level_id()] = level

    async def delete(self, level_id: UUID) -> None:
        del self.__store[level_id]
