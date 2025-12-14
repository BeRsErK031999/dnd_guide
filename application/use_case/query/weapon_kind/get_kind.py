from application.dto.model.weapon_kind import AppWeaponKind
from application.dto.query.weapon_kind import WeaponKindQuery
from application.repository import WeaponKindRepository
from domain.error import DomainError


class GetWeaponKindUseCase:
    def __init__(self, weapon_kind_repository: WeaponKindRepository):
        self._kind_repository = weapon_kind_repository

    async def execute(self, query: WeaponKindQuery) -> AppWeaponKind:
        if not await self._kind_repository.id_exists(query.weapon_kind_id):
            raise DomainError.not_found(
                f"вида оружия с id {query.weapon_kind_id} не существует"
            )
        return await self._kind_repository.get_by_id(query.weapon_kind_id)
