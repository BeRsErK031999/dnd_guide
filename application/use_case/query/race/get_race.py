from application.dto.model.race import AppRace
from application.dto.query.race import RaceQuery
from application.repository import RaceRepository
from domain.error import DomainError


class GetRaceUseCase:
    def __init__(self, race_repository: RaceRepository):
        self.__repository = race_repository

    async def execute(self, query: RaceQuery) -> AppRace:
        if not await self.__repository.id_exists(query.race_id):
            raise DomainError.not_found(f"расы с id {query.race_id} не существует")
        return await self.__repository.get_by_id(query.race_id)
