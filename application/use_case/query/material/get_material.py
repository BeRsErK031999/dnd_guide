from application.dto.model.material import AppMaterial
from application.dto.query.material import MaterialQuery
from application.repository import MaterialRepository
from domain.error import DomainError


class GetMaterialUseCase:
    def __init__(self, material_repository: MaterialRepository) -> None:
        self.__repository = material_repository

    async def execute(self, query: MaterialQuery) -> AppMaterial:
        if not await self.__repository.id_exists(query.material_id):
            raise DomainError.not_found(
                f"материала с id {query.material_id} не существует"
            )
        return await self.__repository.get_by_id(query.material_id)
