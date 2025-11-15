from application.repository import SourceRepository
from domain.source import Source


class GetSourcesUseCase:
    def __init__(self, source_repository: SourceRepository):
        self.__repository = source_repository

    async def execute(self) -> list[Source]:
        return await self.__repository.get_all()
