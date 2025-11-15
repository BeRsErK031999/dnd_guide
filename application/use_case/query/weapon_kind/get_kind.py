from application.dto.query.weapon_kind import WeaponKindQuery
from application.repository import WeaponKindRepository
from domain.error import DomainError
from domain.weapon_kind import WeaponKind


class GetWeaponKindUseCase:
    def __init__(self, weapon_kind_repository: WeaponKindRepository):
        self.__repository = weapon_kind_repository

    async def execute(self, query: WeaponKindQuery) -> WeaponKind:
        if not await self.__repository.id_exists(query.weapon_kind_id):
            raise DomainError.not_found(
                f"вида оружия с id {query.weapon_kind_id} не существует"
            )
        return await self.__repository.get_by_id(query.weapon_kind_id)
