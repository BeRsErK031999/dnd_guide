from abc import ABC, abstractmethod
from uuid import UUID


class SubclassFeatureRepository(ABC):
    @abstractmethod
    async def name_for_class_exists(self, subclass_id: UUID, name: str) -> bool:
        raise NotImplemented
