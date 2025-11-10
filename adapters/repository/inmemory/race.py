from uuid import UUID, uuid4

from application.repository import RaceRepository as AppRaceRepository
from domain.race import Race
from domain.race import RaceRepository as DomainRaceRepository


class InMemoryRaceRepository(DomainRaceRepository, AppRaceRepository):
    def __init__(self) -> None:
        self.__store: dict[UUID, Race] = {}

    async def name_exists(self, name: str) -> bool:
        return any(race.name() == name for race in self.__store.values())

    async def next_id(self) -> UUID:
        return uuid4()

    async def id_exists(self, race_id: UUID) -> bool:
        return race_id in self.__store

    async def get_by_id(self, race_id: UUID) -> Race:
        return self.__store[race_id]

    async def save(self, race: Race) -> None:
        self.__store[race.race_id()] = race

    async def delete(self, race_id: UUID) -> None:
        del self.__store[race_id]
