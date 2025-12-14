from application.dto.model.weapon_kind import AppWeaponKind
from application.dto.query.weapon_kind import WeaponKindsQuery
from application.repository import WeaponKindRepository


class GetWeaponKindsUseCase:
    def __init__(self, weapon_kind_repository: WeaponKindRepository):
        self._kind_repository = weapon_kind_repository

    async def execute(self, query: WeaponKindsQuery) -> list[AppWeaponKind]:
        return await self._kind_repository.filter(
            search_by_name=query.search_by_name, filter_by_types=query.filter_by_types
        )
