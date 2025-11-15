from application.repository import WeaponPropertyRepository
from domain.weapon_property import WeaponProperty


class GetWeaponPropertiesUseCase:
    def __init__(self, weapon_property_repository: WeaponPropertyRepository):
        self.__repository = weapon_property_repository

    async def execute(self) -> list[WeaponProperty]:
        return await self.__repository.get_all()
