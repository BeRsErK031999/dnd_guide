from application.dto.model.weapon_property import AppWeaponProperty
from application.dto.query.weapon_property import WeaponPropertyQuery
from application.repository import WeaponPropertyRepository
from domain.error import DomainError


class GetWeaponPropertyUseCase:
    def __init__(self, weapon_property_repository: WeaponPropertyRepository):
        self._repository = weapon_property_repository

    async def execute(self, query: WeaponPropertyQuery) -> AppWeaponProperty:
        if not await self._repository.id_exists(query.weapon_property_id):
            raise DomainError.not_found(
                f"свойства оружия с id {query.weapon_property_id} не существует"
            )
        return await self._repository.get_by_id(query.weapon_property_id)
