from abc import ABC, abstractmethod
from uuid import UUID

from domain.race import Race


class RaceRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, race_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, race_id: UUID) -> Race:
        raise NotImplemented

    @abstractmethod
    async def save(self, race: Race) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, race_id: UUID) -> None:
        raise NotImplemented
