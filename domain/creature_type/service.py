from domain.creature_type.repository import CreatureTypeRepository


class CreatureTypeService:
    def __init__(self, creature_type_repository: CreatureTypeRepository) -> None:
        self.__repository = creature_type_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
