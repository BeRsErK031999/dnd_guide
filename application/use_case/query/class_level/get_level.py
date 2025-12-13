from application.dto.model.class_level import AppClassLevel
from application.dto.query.class_level import ClassLevelQuery
from application.repository import ClassLevelRepository
from domain.error import DomainError


class GetClassLevelUseCase:
    def __init__(self, class_level_repository: ClassLevelRepository):
        self._repository = class_level_repository

    async def execute(self, query: ClassLevelQuery) -> AppClassLevel:
        if not await self._repository.id_exists(query.class_level_id):
            raise DomainError.not_found(
                f"уровня класса {query.class_level_id} не существует"
            )
        return await self._repository.get_by_id(query.class_level_id)
