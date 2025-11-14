from application.repository import MaterialRepository
from domain.material import Material


class GetMaterialsUseCase:
    def __init__(self, material_repository: MaterialRepository) -> None:
        self.__repository = material_repository

    async def execute(self) -> list[Material]:
        return await self.__repository.get_all()
