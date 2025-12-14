from uuid import UUID, uuid4

from application.dto.model.character_class import AppClass
from application.repository import ClassRepository as AppClassRepository
from domain.character_class import ClassRepository as DomainClassRepository


class InMemoryClassRepository(DomainClassRepository, AppClassRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppClass] = {}

    async def name_exists(self, name: str) -> bool:
        return any(
            character_class.name == name for character_class in self._store.values()
        )

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, class_id: UUID) -> bool:
        return class_id in self._store

    async def get_by_id(self, class_id: UUID) -> AppClass:
        return self._store[class_id]

    async def get_all(self) -> list[AppClass]:
        return list(self._store.values())

    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_source_ids: list[UUID] | None = None,
    ) -> list[AppClass]:
        result: list[AppClass] = list()
        for c in self._store.values():
            if (search_by_name is None or search_by_name in c.name) and (
                filter_by_source_ids is None or c.source_id in filter_by_source_ids
            ):
                result.append(c)
        return result

    async def create(self, character_class: AppClass) -> None:
        self._store[character_class.class_id] = character_class

    async def update(self, character_class: AppClass) -> None:
        self._store[character_class.class_id] = character_class

    async def delete(self, class_id: UUID) -> None:
        del self._store[class_id]
