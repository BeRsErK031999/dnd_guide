from application.repository import ClassLevelRepository
from domain.class_level import ClassLevel


class GetClassLevelsUseCase:
    def __init__(self, class_level_repository: ClassLevelRepository):
        self.__repository = class_level_repository

    async def execute(self) -> list[ClassLevel]:
        return await self.__repository.get_all()
