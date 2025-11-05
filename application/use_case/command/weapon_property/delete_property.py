from application.dto.command.weapon_property import DeleteWeaponPropertyCommand
from application.repository import UserRepository, WeaponPropertyRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteWeaponPropertyUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        weapon_property_repository: WeaponPropertyRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__property_repository = weapon_property_repository

    async def execute(self, command: DeleteWeaponPropertyCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__property_repository.is_weapon_property_of_id_exist(
            command.weapon_property_id
        ):
            raise DomainError.not_found(
                f"свойство с id {command.weapon_property_id} не существует"
            )
        await self.__property_repository.delete(command.weapon_property_id)
