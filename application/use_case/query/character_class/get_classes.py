from application.dto.query.character_class import ClassesQuery
from application.repository import ClassRepository
from domain.character_class import CharacterClass


class GetClassesUseCase:
    def __init__(self, class_repository: ClassRepository):
        self.__repository = class_repository

    async def execute(self, query: ClassesQuery) -> list[CharacterClass]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
