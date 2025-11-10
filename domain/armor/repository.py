from abc import ABC, abstractmethod


class ArmorRepository(ABC):
    @abstractmethod
    async def name_exists(self, name: str) -> bool:
        raise NotImplemented
