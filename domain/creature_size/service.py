from domain.creature_size.repository import CreatureSizeRepository


class CreatureSizeService:
    def __init__(self, creature_size_repository: CreatureSizeRepository) -> None:
        self.__repository = creature_size_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
