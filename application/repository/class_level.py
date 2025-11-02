from abc import ABC, abstractmethod
from uuid import UUID

from domain.class_level.class_level import ClassLevel


class ClassLevelRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_level_of_id_exist(self, level_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_level_of_id(self, level_id: UUID) -> ClassLevel:
        raise NotImplemented

    @abstractmethod
    async def save(self, level: ClassLevel) -> None:
        raise NotImplemented
