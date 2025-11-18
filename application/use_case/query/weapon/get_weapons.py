from application.dto.query.weapon import WeaponsQuery
from application.repository import WeaponRepository
from domain.weapon import Weapon


class GetWeaponsUseCase:
    def __init__(self, weapon_repository: WeaponRepository):
        self.__repository = weapon_repository

    async def execute(self, query: WeaponsQuery) -> list[Weapon]:
        return await self.__repository.filter(
            search_by_name=query.search_by_name,
            filter_by_kind_ids=query.filter_by_kind_ids,
            filter_by_damage_types=query.filter_by_damage_types,
            filter_by_property_ids=query.filter_by_property_ids,
            filter_by_material_ids=query.filter_by_material_ids,
        )
