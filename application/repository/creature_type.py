from abc import ABC, abstractmethod
from uuid import UUID

from domain.creature_type import CreatureType


class CreatureTypeRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_type_of_id_exist(self, creature_type_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_type_of_id(self, creature_type_id: UUID) -> CreatureType:
        raise NotImplemented

    @abstractmethod
    async def save(self, creature_type: CreatureType) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, creature_type_id: UUID) -> None:
        raise NotImplemented
