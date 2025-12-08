from uuid import UUID, uuid4

from application.dto.model.race import AppRace
from application.repository import RaceRepository as AppRaceRepository
from domain.race import RaceRepository as DomainRaceRepository


class InMemoryRaceRepository(DomainRaceRepository, AppRaceRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, AppRace] = {}

    async def name_exists(self, name: str) -> bool:
        return any(race.name == name for race in self._store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, race_id: UUID) -> bool:
        return race_id in self._store

    async def get_by_id(self, race_id: UUID) -> AppRace:
        return self._store[race_id]

    async def get_all(self) -> list[AppRace]:
        return list(self._store.values())

    async def filter(self, search_by_name: str | None = None) -> list[AppRace]:
        if search_by_name is not None:
            return [r for r in self._store.values() if search_by_name in r.name]
        return list(self._store.values())

    async def create(self, race: AppRace) -> None:
        self._store[race.race_id] = race

    async def update(self, race: AppRace) -> None:
        self._store[race.race_id] = race

    async def delete(self, race_id: UUID) -> None:
        del self._store[race_id]
