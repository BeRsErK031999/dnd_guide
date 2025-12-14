from application.dto.command.weapon import DeleteWeaponCommand
from application.repository import ClassRepository, UserRepository, WeaponRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteWeaponUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        weapon_repository: WeaponRepository,
        class_repository: ClassRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._weapon_repository = weapon_repository
        self._class_repository = class_repository

    async def execute(self, command: DeleteWeaponCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._weapon_repository.id_exists(command.weapon_id):
            raise DomainError.not_found(
                f"оружие с id {command.weapon_id} не существует"
            )
        exists_classes = await self._class_repository.filter(
            filter_by_weapon_ids=[command.weapon_id]
        )
        if len(exists_classes) > 0:
            raise DomainError.invalid_data(
                "оружие используется для классов: "
                f"{', '.join(c.name for c in exists_classes)}"
            )
        await self._weapon_repository.delete(command.weapon_id)
