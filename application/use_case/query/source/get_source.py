from application.dto.query.source import SourceQuery
from application.repository import SourceRepository
from domain.error import DomainError
from domain.source import Source


class GetSourceUseCase:
    def __init__(self, source_repository: SourceRepository):
        self.__class_repository = source_repository

    async def execute(self, query: SourceQuery) -> Source:
        if not await self.__class_repository.id_exists(query.source_id):
            raise DomainError.not_found(
                f"источник с id {query.source_id} не существует"
            )
        return await self.__class_repository.get_by_id(query.source_id)
