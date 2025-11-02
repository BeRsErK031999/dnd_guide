from abc import ABC, abstractmethod


class WeaponRepository(ABC):
    @abstractmethod
    async def is_name_exist(self, name: str) -> bool:
        raise NotImplemented
