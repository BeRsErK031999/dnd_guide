from domain.character_subclass.repository import SubclassRepository


class SubclassService:
    def __init__(self, subclass_repository: SubclassRepository) -> None:
        self.__repository = subclass_repository

    async def can_create_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return await self.__repository.is_name_exist(name)
