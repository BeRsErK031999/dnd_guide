from uuid import UUID, uuid4

from application.dto.model.class_level import AppClassLevel
from application.repository import ClassLevelRepository as AppClassLevelRepository
from domain.class_level import ClassLevelRepository as DomainClassLevelRepository


class InMemoryClassLevelRepository(DomainClassLevelRepository, AppClassLevelRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppClassLevel] = {}

    async def level_of_class_exists(self, class_id: UUID, level: int) -> bool:
        return any(
            level == lvl.level
            for lvl in self._store.values()
            if lvl.class_id == class_id
        )

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, level_id: UUID) -> bool:
        return level_id in self._store

    async def get_by_id(self, level_id: UUID) -> AppClassLevel:
        return self._store[level_id]

    async def get_all(self) -> list[AppClassLevel]:
        return list(self._store.values())

    async def filter(
        self, filter_by_class_id: UUID | None = None
    ) -> list[AppClassLevel]:
        if filter_by_class_id is not None:
            return [
                lvl
                for lvl in self._store.values()
                if lvl.class_id == filter_by_class_id
            ]
        return list(self._store.values())

    async def save(self, level: AppClassLevel) -> None:
        self._store[level.class_level_id] = level

    async def delete(self, level_id: UUID) -> None:
        del self._store[level_id]
