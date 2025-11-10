from abc import ABC, abstractmethod
from uuid import UUID

from domain.armor import Armor


class ArmorRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, armor_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, armor_id: UUID) -> Armor:
        raise NotImplemented

    @abstractmethod
    async def save(self, armor: Armor) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, armor_id: UUID) -> None:
        raise NotImplemented
