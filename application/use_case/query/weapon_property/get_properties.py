from application.dto.query.weapon_property import WeaponPropertiesQuery
from application.repository import WeaponPropertyRepository
from domain.weapon_property import WeaponProperty


class GetWeaponPropertiesUseCase:
    def __init__(self, weapon_property_repository: WeaponPropertyRepository):
        self.__repository = weapon_property_repository

    async def execute(self, query: WeaponPropertiesQuery) -> list[WeaponProperty]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
