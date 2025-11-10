from abc import ABC, abstractmethod
from uuid import UUID

from domain.weapon_property import WeaponProperty


class WeaponPropertyRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, weapon_property_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, weapon_property_id: UUID) -> WeaponProperty:
        raise NotImplemented

    @abstractmethod
    async def save(self, weapon_property: WeaponProperty) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, weapon_property_id: UUID) -> None:
        raise NotImplemented
