from application.repository import CreatureTypeRepository
from domain.creature_type import CreatureType


class GetCreatureTypesUseCase:
    def __init__(self, creature_type_repository: CreatureTypeRepository):
        self.__repository = creature_type_repository

    async def execute(self) -> list[CreatureType]:
        return await self.__repository.get_all()
