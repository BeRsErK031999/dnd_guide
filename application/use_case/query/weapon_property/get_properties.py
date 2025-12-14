from application.dto.model.weapon_property import AppWeaponProperty
from application.dto.query.weapon_property import WeaponPropertiesQuery
from application.repository import WeaponPropertyRepository


class GetWeaponPropertiesUseCase:
    def __init__(self, weapon_property_repository: WeaponPropertyRepository):
        self._repository = weapon_property_repository

    async def execute(self, query: WeaponPropertiesQuery) -> list[AppWeaponProperty]:
        return await self._repository.filter(search_by_name=query.search_by_name)
