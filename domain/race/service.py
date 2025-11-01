from domain.race.repository import RaceRepository


class RaceService:
    def __init__(self, race_repository: RaceRepository) -> None:
        self.__repository = race_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
