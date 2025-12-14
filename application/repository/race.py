from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.model.race import AppRace


class RaceRepository(ABC):
    @abstractmethod
    async def next_id(self) -> UUID:
        raise NotImplemented

    @abstractmethod
    async def id_exists(self, race_id: UUID) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, race_id: UUID) -> AppRace:
        raise NotImplemented

    @abstractmethod
    async def get_all(self) -> list[AppRace]:
        raise NotImplemented

    @abstractmethod
    async def filter(
        self,
        search_by_name: str | None = None,
        filter_by_source_ids: list[UUID] | None = None,
    ) -> list[AppRace]:
        raise NotImplemented

    @abstractmethod
    async def create(self, race: AppRace) -> None:
        raise NotImplemented

    @abstractmethod
    async def update(self, race: AppRace) -> None:
        raise NotImplemented

    @abstractmethod
    async def delete(self, race_id: UUID) -> None:
        raise NotImplemented
