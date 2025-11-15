from application.repository import SubraceRepository
from domain.subrace import Subrace


class GetSubracesUseCase:
    def __init__(self, subrace_repository: SubraceRepository):
        self.__repository = subrace_repository

    async def execute(self) -> list[Subrace]:
        return await self.__repository.get_all()
