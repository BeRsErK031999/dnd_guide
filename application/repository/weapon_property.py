from abc import ABC, abstractmethod
from uuid import UUID

from domain.weapon_property.weapon_property import WeaponProperty


class WeaponPropertyRepository(ABC):
    @abstractmethod
    def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_weapon_property_of_id_exist(self, weapon_property_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_weapon_property_of_id(
        self, weapon_property_id: UUID
    ) -> WeaponProperty:
        raise NotImplemented

    @abstractmethod
    async def save(self, weapon_property: WeaponProperty) -> None:
        raise NotImplemented
