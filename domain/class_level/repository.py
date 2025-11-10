from abc import ABC, abstractmethod
from uuid import UUID


class ClassLevelRepository(ABC):
    @abstractmethod
    async def level_of_class_exists(self, class_id: UUID, level: int) -> bool:
        raise NotImplemented
