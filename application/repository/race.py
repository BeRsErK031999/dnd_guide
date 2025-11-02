from abc import ABC, abstractmethod
from uuid import UUID

from domain.race.race import Race


class RaceRepository(ABC):
    @abstractmethod
    def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def is_race_of_id_exist(self, race_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_race_of_id(self, race_id: UUID) -> Race:
        raise NotImplemented

    @abstractmethod
    async def save(self, race: Race) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, race_id: UUID) -> None:
        raise NotImplemented
