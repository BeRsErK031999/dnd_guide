from application.repository import MaterialComponentRepository
from domain.material_component import MaterialComponent


class GetMaterialComponentsUseCase:
    def __init__(self, material_repository: MaterialComponentRepository):
        self.__repository = material_repository

    async def execute(self) -> list[MaterialComponent]:
        return await self.__repository.get_all()
