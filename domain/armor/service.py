from domain.armor.repository import ArmorRepository


class ArmorService:
    def __init__(self, armor_repository: ArmorRepository) -> None:
        self.__repository = armor_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
