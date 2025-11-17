from application.dto.query.class_level import ClassLevelsQuery
from application.repository import ClassLevelRepository
from domain.class_level import ClassLevel


class GetClassLevelsUseCase:
    def __init__(self, class_level_repository: ClassLevelRepository):
        self.__repository = class_level_repository

    async def execute(self, query: ClassLevelsQuery) -> list[ClassLevel]:
        return await self.__repository.filter(
            filter_by_class_id=query.filter_by_class_id
        )
