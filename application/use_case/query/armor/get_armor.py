from application.dto.model.armor import AppArmor
from application.dto.query.armor import ArmorQuery
from application.repository import ArmorRepository
from domain.error import DomainError


class GetArmorUseCase:
    def __init__(self, armor_repository: ArmorRepository):
        self._repository = armor_repository

    async def execute(self, query: ArmorQuery) -> AppArmor:
        if not await self._repository.id_exists(query.armor_id):
            raise DomainError.not_found(f"доспехов с id {query.armor_id} не существует")
        return await self._repository.get_by_id(query.armor_id)
