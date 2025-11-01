from abc import ABC, abstractmethod


class ClassFeatureRepository(ABC):
    @abstractmethod
    async def is_name_exist(self, name: str) -> bool:
        raise NotImplemented
