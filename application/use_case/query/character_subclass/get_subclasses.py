from application.dto.model.character_subclass import AppSubclass
from application.dto.query.character_subclass import SubclassesQuery
from application.repository import SubclassRepository


class GetSubclassesUseCase:
    def __init__(self, subclass_repository: SubclassRepository):
        self.__repository = subclass_repository

    async def execute(self, query: SubclassesQuery) -> list[AppSubclass]:
        return await self.__repository.filter(
            filter_by_class_id=query.filter_by_class_id
        )
