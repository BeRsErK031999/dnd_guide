from application.dto.model.character_subclass import AppSubclass
from application.dto.query.character_subclass import SubclassQuery
from application.repository import SubclassRepository
from domain.error import DomainError


class GetSubclassUseCase:
    def __init__(self, subclass_repository: SubclassRepository):
        self.__repository = subclass_repository

    async def execute(self, query: SubclassQuery) -> AppSubclass:
        if not await self.__repository.id_exists(query.subclass_id):
            raise DomainError.not_found(
                f"подкласс с id {query.subclass_id} не существует"
            )
        return await self.__repository.get_by_id(query.subclass_id)
