from abc import ABC, abstractmethod
from uuid import UUID

from domain.weapon_kind.weapon_kind import WeaponKind


class WeaponKindRepository(ABC):
    @abstractmethod
    def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_weapon_kind_of_id_exist(self, weapon_kind_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_weapon_kind_of_id(self, weapon_kind_id: UUID) -> WeaponKind:
        raise NotImplemented

    @abstractmethod
    async def save(self, weapon_kind: WeaponKind) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, weapon_kind_id: UUID) -> None:
        raise NotImplemented
