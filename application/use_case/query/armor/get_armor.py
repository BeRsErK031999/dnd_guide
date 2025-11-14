from application.dto.query.armor import ArmorQuery
from application.repository import ArmorRepository
from domain.armor import Armor


class GetArmorUseCase:
    def __init__(self, repository: ArmorRepository):
        self.__repository = repository

    async def execute(self, query: ArmorQuery) -> Armor:
        return await self.__repository.get_by_id(query.armor_id)
