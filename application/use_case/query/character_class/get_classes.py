from application.repository import ClassRepository
from domain.character_class import CharacterClass


class GetClassesUseCase:
    def __init__(self, class_repository: ClassRepository):
        self.__repository = class_repository

    async def execute(self) -> list[CharacterClass]:
        return await self.__repository.get_all()
