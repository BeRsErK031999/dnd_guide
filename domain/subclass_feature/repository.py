from abc import ABC, abstractmethod
from uuid import UUID


class SubclassFeatureRepository(ABC):
    @abstractmethod
    async def is_name_for_class_exist(self, subclass_id: UUID, name: str) -> bool:
        raise NotImplemented
