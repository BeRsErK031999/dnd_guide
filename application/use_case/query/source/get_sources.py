from application.dto.query.source import SourcesQuery
from application.repository import SourceRepository
from domain.source import Source


class GetSourcesUseCase:
    def __init__(self, source_repository: SourceRepository):
        self.__repository = source_repository

    async def execute(self, query: SourcesQuery) -> list[Source]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
