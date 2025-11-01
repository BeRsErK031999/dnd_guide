from abc import ABC, abstractmethod
from uuid import UUID


class ClassFeatureRepository(ABC):
    @abstractmethod
    async def is_name_for_class_exist(self, class_id: UUID, name: str) -> bool:
        raise NotImplemented
