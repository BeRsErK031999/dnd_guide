from abc import ABC, abstractmethod


class RaceRepository(ABC):
    @abstractmethod
    async def name_exists(self, name: str) -> bool:
        raise NotImplemented
