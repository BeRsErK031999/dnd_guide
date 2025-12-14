from application.dto.command.race import DeleteRaceCommand
from application.repository import RaceRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteRaceUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        race_repository: RaceRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._race_repository = race_repository

    async def execute(self, command: DeleteRaceCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._race_repository.id_exists(command.race_id):
            raise DomainError.not_found(f"расы с id {command.race_id} не существует")
        await self._race_repository.delete(command.race_id)
