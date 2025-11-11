from abc import ABC, abstractmethod
from uuid import UUID

from domain.class_level import ClassLevel


class ClassLevelRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, level_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, level_id: UUID) -> ClassLevel:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[ClassLevel]:
        raise NotImplemented

    @abstractmethod
    async def create(self, level: ClassLevel) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, level: ClassLevel) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, level_id: UUID) -> None:
        raise NotImplemented
