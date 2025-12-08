from domain.race.repository import RaceRepository


class RaceService:
    def __init__(self, race_repository: RaceRepository) -> None:
        self._repository = race_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self._repository.name_exists(name)
