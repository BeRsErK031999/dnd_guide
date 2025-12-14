from application.dto.model.weapon import AppWeapon
from application.dto.query.weapon import WeaponQuery
from application.repository import WeaponRepository
from domain.error import DomainError


class GetWeaponUseCase:
    def __init__(self, weapon_repository: WeaponRepository):
        self._repository = weapon_repository

    async def execute(self, query: WeaponQuery) -> AppWeapon:
        if not await self._repository.id_exists(query.weapon_id):
            raise DomainError.not_found(f"оружия с id {query.weapon_id} не существует")
        return await self._repository.get_by_id(query.weapon_id)
