from application.dto.command.creature_size import CreateCreatureSizeCommand
from application.repository import CreatureSizeRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.creature_size import CreatureSize, CreatureSizeService
from domain.error import DomainError


class CreateCreatureSizeUseCase(UserCheck):
    def __init__(
        self,
        creature_size_service: CreatureSizeService,
        user_repository: UserRepository,
        creature_size_repository: CreatureSizeRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__size_repository = creature_size_repository
        self.__size_service = creature_size_service

    async def execute(self, command: CreateCreatureSizeCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__size_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать размер существа с название {command.name}"
            )
        size = CreatureSize(
            await self.__size_repository.next_id(), command.name, command.description
        )
        await self.__size_repository.create(size)
