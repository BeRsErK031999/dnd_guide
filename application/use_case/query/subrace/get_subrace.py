from application.dto.model.subrace import AppSubrace
from application.dto.query.subrace import SubraceQuery
from application.repository import SubraceRepository
from domain.error import DomainError


class GetSubraceUseCase:
    def __init__(self, subrace_repository: SubraceRepository):
        self.__repository = subrace_repository

    async def execute(self, query: SubraceQuery) -> AppSubrace:
        if not await self.__repository.id_exists(query.subrace_id):
            raise DomainError.not_found(
                f"подрасы с id {query.subrace_id} не существует"
            )
        return await self.__repository.get_by_id(query.subrace_id)
