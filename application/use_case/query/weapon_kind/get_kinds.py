from application.dto.query.weapon_kind import WeaponKindsQuery
from application.repository import WeaponKindRepository
from domain.weapon_kind import WeaponKind


class GetWeaponKindsUseCase:
    def __init__(self, weapon_kind_repository: WeaponKindRepository):
        self.__repository = weapon_kind_repository

    async def execute(self, query: WeaponKindsQuery) -> list[WeaponKind]:
        return await self.__repository.filter(
            search_by_name=query.search_by_name, filter_by_types=query.filter_by_types
        )
