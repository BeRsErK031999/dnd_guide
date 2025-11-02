from domain.weapon_kind.repository import WeaponKindRepository


class WeaponKindService:
    def __init__(self, weapon_kind_repository: WeaponKindRepository) -> None:
        self.__repository = weapon_kind_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
