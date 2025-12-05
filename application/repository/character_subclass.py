from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.character_subclass import AppSubclass


class SubclassRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, subclass_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, subclass_id: UUID) -> AppSubclass:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppSubclass]:
        raise NotImplemented

    @abstractmethod
    async def filter(self, filter_by_class_id: UUID | None = None) -> list[AppSubclass]:
        raise NotImplemented

    @abstractmethod
    async def create(self, subclass: AppSubclass) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, subclass: AppSubclass) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, subclass_id: UUID) -> None:
        raise NotImplemented
