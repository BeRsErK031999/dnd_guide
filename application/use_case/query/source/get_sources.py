from application.dto.model.source import AppSource
from application.dto.query.source import SourcesQuery
from application.repository import SourceRepository


class GetSourcesUseCase:
    def __init__(self, source_repository: SourceRepository):
        self._source_repository = source_repository

    async def execute(self, query: SourcesQuery) -> list[AppSource]:
        return await self._source_repository.filter(search_by_name=query.search_by_name)
