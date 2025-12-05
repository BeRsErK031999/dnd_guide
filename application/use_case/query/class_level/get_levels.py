from application.dto.model.class_level import AppClassLevel
from application.dto.query.class_level import ClassLevelsQuery
from application.repository import ClassLevelRepository


class GetClassLevelsUseCase:
    def __init__(self, class_level_repository: ClassLevelRepository):
        self.__repository = class_level_repository

    async def execute(self, query: ClassLevelsQuery) -> list[AppClassLevel]:
        return await self.__repository.filter(
            filter_by_class_id=query.filter_by_class_id
        )
