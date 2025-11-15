from application.repository import RaceRepository
from domain.race import Race


class GetRacesUseCase:
    def __init__(self, race_repository: RaceRepository):
        self.__repository = race_repository

    async def execute(self) -> list[Race]:
        return await self.__repository.get_all()
