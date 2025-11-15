from application.repository import SubclassRepository
from domain.character_subclass import CharacterSubclass


class GetSubclassesUseCase:
    def __init__(self, subclass_repository: SubclassRepository):
        self.__repository = subclass_repository

    async def execute(self) -> list[CharacterSubclass]:
        return await self.__repository.get_all()
