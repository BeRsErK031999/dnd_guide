from application.dto.command.weapon_kind import DeleteWeaponKindCommand
from application.repository import (
    UserRepository,
    WeaponKindRepository,
    WeaponRepository,
)
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteWeaponKindUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        weapon_kind_repository: WeaponKindRepository,
        weapon_repository: WeaponRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._kind_repository = weapon_kind_repository
        self._weapon_repository = weapon_repository

    async def execute(self, command: DeleteWeaponKindCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._kind_repository.id_exists(command.weapon_kind_id):
            raise DomainError.not_found(
                f"вид оружия с id {command.weapon_kind_id} не существует"
            )
        exists_weapons = await self._weapon_repository.filter(
            filter_by_kind_ids=[command.weapon_kind_id]
        )
        if len(exists_weapons) > 0:
            raise DomainError.invalid_data(
                "вид оружия используется в оружии: "
                f"{", ".join([w.name for w in exists_weapons])}"
            )
        await self._kind_repository.delete(command.weapon_kind_id)
