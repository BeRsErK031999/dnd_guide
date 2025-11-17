from application.dto.query.material import MaterialsQuery
from application.repository import MaterialRepository
from domain.material import Material


class GetMaterialsUseCase:
    def __init__(self, material_repository: MaterialRepository) -> None:
        self.__repository = material_repository

    async def execute(self, query: MaterialsQuery) -> list[Material]:
        if query.search_by_name is None:
            return await self.__repository.get_all()
        return await self.__repository.filter(query.search_by_name)
