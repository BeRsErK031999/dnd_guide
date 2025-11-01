from uuid import UUID

from domain.class_level.repository import ClassLevelRepository


class ClassLevelService:
    def __init__(self, class_level_repository: ClassLevelRepository) -> None:
        self.__repository = class_level_repository

    async def can_create_with_class_and_level(self, class_id: UUID, level: int) -> bool:
        return await self.__repository.is_level_of_class_exist(class_id, level)

    async def can_change_level_of_class(self, class_id: UUID, level: int) -> bool:
        return await self.__repository.is_level_of_class_exist(class_id, level)
