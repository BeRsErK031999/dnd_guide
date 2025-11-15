from application.dto.query.creature_size import CreatureSizeQuery
from application.repository import CreatureSizeRepository
from domain.creature_size import CreatureSize
from domain.error import DomainError


class GetCreatureSizeUseCase:
    def __init__(self, creature_size_repository: CreatureSizeRepository):
        self.__repository = creature_size_repository

    async def execute(self, query: CreatureSizeQuery) -> CreatureSize:
        if not await self.__repository.id_exists(query.size_id):
            raise DomainError.not_found(
                f"размера существа с id {query.size_id} не существует"
            )
        return await self.__repository.get_by_id(query.size_id)
