from abc import ABC, abstractmethod
from uuid import UUID


class ClassLevelRepository(ABC):
    @abstractmethod
    async def is_level_of_class_exist(self, class_id: UUID, level: int) -> bool:
        raise NotImplemented
