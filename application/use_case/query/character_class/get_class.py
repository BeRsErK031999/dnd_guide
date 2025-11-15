from application.dto.query.character_class import ClassQuery
from application.repository import ClassRepository
from domain.character_class import CharacterClass
from domain.error import DomainError


class GetClassUseCase:
    def __init__(self, class_repository: ClassRepository):
        self.__class_repository = class_repository

    async def execute(self, query: ClassQuery) -> CharacterClass:
        if not await self.__class_repository.id_exists(query.class_id):
            raise DomainError.not_found(f"класса с id {query.class_id} не существует")
        return await self.__class_repository.get_by_id(query.class_id)
