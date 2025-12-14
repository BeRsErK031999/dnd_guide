from application.dto.command.weapon_property import DeleteWeaponPropertyCommand
from application.repository import (
    UserRepository,
    WeaponPropertyRepository,
    WeaponRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteWeaponPropertyUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        weapon_property_repository: WeaponPropertyRepository,
        weapon_repository: WeaponRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._property_repository = weapon_property_repository
        self._weapon_repository = weapon_repository

    async def execute(self, command: DeleteWeaponPropertyCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._property_repository.id_exists(command.weapon_property_id):
            raise DomainError.not_found(
                f"свойство с id {command.weapon_property_id} не существует"
            )
        exists_weapons = await self._weapon_repository.filter(
            filter_by_property_ids=[command.weapon_property_id]
        )
        if len(exists_weapons) > 0:
            raise DomainError.invalid_data(
                "свойство используется в оружии: "
                f"{", ".join([w.name for w in exists_weapons])}"
            )
        await self._property_repository.delete(command.weapon_property_id)
