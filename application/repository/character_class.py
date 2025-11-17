from abc import ABC, abstractmethod
from uuid import UUID

from domain.character_class import CharacterClass


class ClassRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, class_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, class_id: UUID) -> CharacterClass:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[CharacterClass]:
        raise NotImplemented

    @abstractmethod
    async def filter(self, search_by_name: str | None = None) -> list[CharacterClass]:
        raise NotImplemented

    @abstractmethod
    async def create(self, character_class: CharacterClass) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, character_class: CharacterClass) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, class_id: UUID) -> None:
        raise NotImplemented
