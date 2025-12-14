from application.dto.model.source import AppSource
from application.dto.query.source import SourceQuery
from application.repository import SourceRepository
from domain.error import DomainError


class GetSourceUseCase:
    def __init__(self, source_repository: SourceRepository):
        self._source_repository = source_repository

    async def execute(self, query: SourceQuery) -> AppSource:
        if not await self._source_repository.id_exists(query.source_id):
            raise DomainError.not_found(
                f"источник с id {query.source_id} не существует"
            )
        return await self._source_repository.get_by_id(query.source_id)
