from application.dto.command.spell import DeleteSpellCommand
from application.repository import SpellRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteSpellUseCase(UserCheck):
    def __init__(
        self, user_repository: UserRepository, spell_repository: SpellRepository
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__spell_repository = spell_repository

    async def execute(self, command: DeleteSpellCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__spell_repository.id_exists(command.spell_id):
            raise DomainError.not_found(
                f"заклинание с id {command.spell_id} не существует"
            )
        await self.__spell_repository.delete(command.spell_id)
