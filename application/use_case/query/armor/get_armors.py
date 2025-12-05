from application.dto.model.armor import AppArmor
from application.dto.query.armor import ArmorsQuery
from application.repository import ArmorRepository


class GetArmorsUseCase:
    def __init__(self, armor_repository: ArmorRepository):
        self.__repository = armor_repository

    async def execute(self, query: ArmorsQuery) -> list[AppArmor]:
        return await self.__repository.filter(
            search_by_name=query.search_by_name,
            filter_by_armor_types=query.filter_by_armor_types,
            filter_by_material_ids=query.filter_by_material_ids,
        )
