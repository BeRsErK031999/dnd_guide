from application.dto.query.armor import ArmorsQuery
from application.repository import ArmorRepository
from domain.armor import Armor


class GetArmorsUseCase:
    def __init__(self, armor_repository: ArmorRepository):
        self.__repository = armor_repository

    async def execute(self, query: ArmorsQuery) -> list[Armor]:
        return await self.__repository.filter(
            search_by_name=query.search_by_name,
            filter_by_armor_type=query.filter_by_armor_type,
            filter_by_material_id=query.filter_by_material_id,
        )
