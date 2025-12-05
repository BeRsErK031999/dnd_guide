from application.dto.model.subrace import AppSubrace
from application.dto.query.subrace import SubracesQuery
from application.repository import SubraceRepository


class GetSubracesUseCase:
    def __init__(self, subrace_repository: SubraceRepository):
        self.__repository = subrace_repository

    async def execute(self, query: SubracesQuery) -> list[AppSubrace]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
