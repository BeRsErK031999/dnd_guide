from application.dto.model.character_class import AppClass
from application.dto.query.character_class import ClassQuery
from application.repository import ClassRepository
from domain.error import DomainError


class GetClassUseCase:
    def __init__(self, class_repository: ClassRepository):
        self._class_repository = class_repository

    async def execute(self, query: ClassQuery) -> AppClass:
        if not await self._class_repository.id_exists(query.class_id):
            raise DomainError.not_found(f"класса с id {query.class_id} не существует")
        return await self._class_repository.get_by_id(query.class_id)
