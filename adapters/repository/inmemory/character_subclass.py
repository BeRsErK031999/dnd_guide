from typing import Dict
from uuid import UUID, uuid4

from application.dto.model.character_subclass import AppSubclass
from application.repository import SubclassRepository as AppSubclassRepository
from domain.character_subclass import SubclassRepository as DomainSubclassRepository


class InMemorySubclassRepository(DomainSubclassRepository, AppSubclassRepository):
    def __init__(self) -> None:
        self._store: Dict[UUID, AppSubclass] = {}

    async def name_exists(self, name: str) -> bool:
        return any(armor.name == name for armor in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, subclass_id: UUID) -> bool:
        return subclass_id in self._store

    async def get_by_id(self, subclass_id: UUID) -> AppSubclass:
        return self._store[subclass_id]

    async def get_all(self) -> list[AppSubclass]:
        return list(self._store.values())

    async def filter(self, filter_by_class_id: UUID | None = None) -> list[AppSubclass]:
        if filter_by_class_id is not None:
            return [
                subclass
                for subclass in self._store.values()
                if subclass.class_id == filter_by_class_id
            ]
        else:
            return list(self._store.values())

    async def save(self, subclass: AppSubclass) -> None:
        self._store[subclass.subclass_id] = subclass

    async def delete(self, subclass_id: UUID) -> None:
        del self._store[subclass_id]
