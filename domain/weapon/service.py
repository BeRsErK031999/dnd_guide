from domain.weapon.repository import WeaponRepository


class WeaponService:
    def __init__(self, weapon_repository: WeaponRepository) -> None:
        self.__repository = weapon_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
