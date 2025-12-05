from application.dto.model.material_component import AppMaterialComponent
from application.dto.query.material_component import MaterialComponentsQuery
from application.repository import MaterialComponentRepository


class GetMaterialComponentsUseCase:
    def __init__(self, material_repository: MaterialComponentRepository):
        self.__repository = material_repository

    async def execute(
        self, query: MaterialComponentsQuery
    ) -> list[AppMaterialComponent]:
        return await self.__repository.filter(search_by_name=query.search_by_name)
