from abc import ABC, abstractmethod
from uuid import UUID

from domain.character_subclass import CharacterSubclass


class SubclassRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, subclass_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, subclass_id: UUID) -> CharacterSubclass:
        raise NotImplemented

    @abstractmethod
    async def save(self, subclass: CharacterSubclass) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, subclass_id: UUID) -> None:
        raise NotImplemented
