from application.dto.model.character_class import AppClass
from application.dto.query.character_class import ClassesQuery
from application.repository import ClassRepository


class GetClassesUseCase:
    def __init__(self, class_repository: ClassRepository):
        self.__repository = class_repository

    async def execute(self, query: ClassesQuery) -> list[AppClass]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
