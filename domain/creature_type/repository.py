from abc import ABC, abstractmethod


class CreatureTypeRepository(ABC):
    @abstractmethod
    async def name_exists(self, name: str) -> bool:
        raise NotImplemented
