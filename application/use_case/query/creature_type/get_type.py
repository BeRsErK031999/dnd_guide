from application.dto.query.creature_type import CreatureTypeQuery
from application.repository import CreatureTypeRepository
from domain.creature_type import CreatureType
from domain.error import DomainError


class GetCreatureTypeUseCase:
    def __init__(self, creature_type_repository: CreatureTypeRepository):
        self.__repository = creature_type_repository

    async def execute(self, query: CreatureTypeQuery) -> CreatureType:
        if not await self.__repository.id_exists(query.type_id):
            raise DomainError.not_found(
                f"типа существа с id {query.type_id} не существует"
            )
        return await self.__repository.get_by_id(query.type_id)
