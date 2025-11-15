from application.repository import CreatureSizeRepository
from domain.creature_size import CreatureSize


class GetCreatureSizesUseCase:
    def __init__(self, creature_size_repository: CreatureSizeRepository):
        self.__repository = creature_size_repository

    async def execute(self) -> list[CreatureSize]:
        return await self.__repository.get_all()
