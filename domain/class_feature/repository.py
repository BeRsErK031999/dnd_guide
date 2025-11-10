from abc import ABC, abstractmethod
from uuid import UUID


class ClassFeatureRepository(ABC):
    @abstractmethod
    async def name_for_class_exists(self, class_id: UUID, name: str) -> bool:
        raise NotImplemented
