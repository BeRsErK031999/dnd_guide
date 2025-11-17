from application.dto.query.race import RacesQuery
from application.repository import RaceRepository
from domain.race import Race


class GetRacesUseCase:
    def __init__(self, race_repository: RaceRepository):
        self.__repository = race_repository

    async def execute(self, query: RacesQuery) -> list[Race]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
