from application.dto.command.weapon_kind import CreateWeaponKindCommand
from application.repository import UserRepository, WeaponKindRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.weapon_kind import WeaponKind, WeaponKindService, WeaponType


class CreateWeaponKindUseCase(UserCheck):
    def __init__(
        self,
        weapon_kind_service: WeaponKindService,
        user_repository: UserRepository,
        weapon_kind_repository: WeaponKindRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__kind_service = weapon_kind_service
        self.__kind_repository = weapon_kind_repository

    async def execute(self, command: CreateWeaponKindCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__kind_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"вид оружия с названием {command.name} не возможно создать"
            )
        kind = WeaponKind(
            await self.__kind_repository.next_id(),
            command.name,
            command.description,
            WeaponType.from_str(command.weapon_type),
        )
        await self.__kind_repository.create(kind)
