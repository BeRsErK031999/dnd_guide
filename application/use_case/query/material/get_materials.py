from application.dto.query.material import MaterialsQuery
from application.repository import MaterialRepository
from domain.material import Material


class GetMaterialsUseCase:
    def __init__(self, material_repository: MaterialRepository) -> None:
        self.__repository = material_repository

    async def execute(self, query: MaterialsQuery) -> list[Material]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
