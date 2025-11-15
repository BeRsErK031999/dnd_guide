from application.dto.query.weapon import WeaponQuery
from application.repository import WeaponRepository
from domain.error import DomainError
from domain.weapon import Weapon


class GetWeaponUseCase:
    def __init__(self, weapon_repository: WeaponRepository):
        self.__repository = weapon_repository

    async def execute(self, query: WeaponQuery) -> Weapon:
        if not await self.__repository.id_exists(query.weapon_id):
            raise DomainError.not_found(f"оружия с id {query.weapon_id} не существует")
        return await self.__repository.get_by_id(query.weapon_id)
