from abc import ABC, abstractmethod
from uuid import UUID

from domain.character_class import CharacterClass


class ClassRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_class_of_id_exist(self, class_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_class_of_id(self, class_id: UUID) -> CharacterClass:
        raise NotImplemented

    @abstractmethod
    async def save(self, character_class: CharacterClass) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, class_id: UUID) -> None:
        raise NotImplemented
