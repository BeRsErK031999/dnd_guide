from domain.character_class.repository import ClassRepository


class ClassService:
    def __init__(self, class_repository: ClassRepository) -> None:
        self.__repository = class_repository

    async def can_create_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)

    async def can_rename_with_name(self, name: str) -> bool:
        return not await self.__repository.name_exists(name)
