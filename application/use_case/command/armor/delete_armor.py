from application.dto.command.armor import DeleteArmorCommand
from application.repository import ArmorRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteArmorUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        armor_repository: ArmorRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._armor_repository = armor_repository

    async def execute(self, command: DeleteArmorCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._armor_repository.id_exists(command.armor_id):
            raise DomainError.not_found(
                f"доспехов с id {command.armor_id} не существует"
            )
        await self._armor_repository.delete(command.armor_id)
