from abc import ABC, abstractmethod
from uuid import UUID

from domain.weapon import Weapon


class WeaponRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, weapon_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, weapon_id: UUID) -> Weapon:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[Weapon]:
        raise NotImplemented

    @abstractmethod
    async def save(self, weapon: Weapon) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, weapon_id: UUID) -> None:
        raise NotImplemented
