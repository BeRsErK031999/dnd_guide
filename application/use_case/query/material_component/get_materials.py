from application.dto.query.material_component import MaterialComponentsQuery
from application.repository import MaterialComponentRepository
from domain.material_component import MaterialComponent


class GetMaterialComponentsUseCase:
    def __init__(self, material_repository: MaterialComponentRepository):
        self.__repository = material_repository

    async def execute(self, query: MaterialComponentsQuery) -> list[MaterialComponent]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
