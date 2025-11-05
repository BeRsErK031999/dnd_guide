from application.dto.command.weapon_kind import DeleteWeaponKindCommand
from application.repository import UserRepository, WeaponKindRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteWeaponKindUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        weapon_kind_repository: WeaponKindRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__kind_repository = weapon_kind_repository

    async def execute(self, command: DeleteWeaponKindCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__kind_repository.is_weapon_kind_of_id_exist(
            command.weapon_kind_id
        ):
            raise DomainError.not_found(
                f"вид оружия с id {command.weapon_kind_id} не существует"
            )
        await self.__kind_repository.delete(command.weapon_kind_id)
