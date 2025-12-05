from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.class_level import AppClassLevel


class ClassLevelRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, level_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, level_id: UUID) -> AppClassLevel:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppClassLevel]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self, filter_by_class_id: UUID | None = None
    ) -> list[AppClassLevel]:
        raise NotImplemented

    @abstractmethod
    async def create(self, level: AppClassLevel) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, level: AppClassLevel) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, level_id: UUID) -> None:
        raise NotImplemented
