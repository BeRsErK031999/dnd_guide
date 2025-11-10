from domain.weapon_property.repository import WeaponPropertyRepository


class WeaponPropertyService:
    def __init__(self, weapon_kind_repository: WeaponPropertyRepository) -> None:
        self.__repository = weapon_kind_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)
