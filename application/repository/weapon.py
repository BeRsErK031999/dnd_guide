from abc import ABC, abstractmethod
from uuid import UUID

from domain.weapon.weapon import Weapon


class WeaponRepository(ABC):
    @abstractmethod
    def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_weapon_of_id_exist(self, weapon_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_weapon_of_id(self, weapon_id: UUID) -> Weapon:
        raise NotImplemented

    @abstractmethod
    async def save(self, weapon: Weapon) -> None:
        raise NotImplemented
