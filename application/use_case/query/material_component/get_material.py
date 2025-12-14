from application.dto.model.material_component import AppMaterialComponent
from application.dto.query.material_component import MaterialComponentQuery
from application.repository import MaterialComponentRepository
from domain.error import DomainError


class GetMaterialComponentUseCase:
    def __init__(self, material_repository: MaterialComponentRepository):
        self._repository = material_repository

    async def execute(self, query: MaterialComponentQuery) -> AppMaterialComponent:
        if not await self._repository.id_exists(query.material_id):
            raise DomainError.not_found(
                f"материала с id {query.material_id} не существует"
            )
        return await self._repository.get_by_id(query.material_id)
