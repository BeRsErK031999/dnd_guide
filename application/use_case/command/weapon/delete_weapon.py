from application.dto.command.weapon import DeleteWeaponCommand
from application.repository import UserRepository, WeaponRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteWeaponUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        weapon_repository: WeaponRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__weapon_repository = weapon_repository

    async def execute(self, command: DeleteWeaponCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__weapon_repository.id_exists(command.weapon_id):
            raise DomainError.not_found(
                f"оружие с id {command.weapon_id} не существует"
            )
        await self.__weapon_repository.delete(command.weapon_id)
