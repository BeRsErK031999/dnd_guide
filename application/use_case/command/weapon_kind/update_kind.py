from application.dto.command.weapon_kind import UpdateWeaponKindCommand
from application.dto.model.weapon_kind import AppWeaponKind
from application.repository import UserRepository, WeaponKindRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.weapon_kind import WeaponKindService, WeaponType


class UpdateWeaponKindUseCase(UserCheck):
    def __init__(
        self,
        weapon_kind_service: WeaponKindService,
        user_repository: UserRepository,
        weapon_kind_repository: WeaponKindRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__kind_service = weapon_kind_service
        self.__kind_repository = weapon_kind_repository

    async def execute(self, command: UpdateWeaponKindCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__kind_repository.id_exists(command.weapon_kind_id):
            raise DomainError.not_found(
                f"вид оружия с id {command.weapon_kind_id} не существует"
            )
        app_kind = await self.__kind_repository.get_by_id(command.weapon_kind_id)
        kind = app_kind.to_domain()
        if command.weapon_type is not None:
            kind.new_weapon_type(WeaponType.from_str(command.weapon_type))
        if command.name is not None:
            if not await self.__kind_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"вид оружия не возможно переименовать с названием {command.name}"
                )
            kind.new_name(command.name)
        if command.description is not None:
            kind.new_description(command.description)
        await self.__kind_repository.update(AppWeaponKind.from_domain(kind))
