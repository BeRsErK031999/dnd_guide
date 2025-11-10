from abc import ABC, abstractmethod


class WeaponKindRepository(ABC):
    @abstractmethod
    async def name_exists(self, name: str) -> bool:
        raise NotImplemented
