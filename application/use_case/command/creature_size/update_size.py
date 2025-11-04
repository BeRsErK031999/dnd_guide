from application.dto.command.creature_size import UpdateCreatureSizeCommand
from application.repository import CreatureSizeRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.creature_size import CreatureSizeService
from domain.error import DomainError


class UpdateCreatureSizeUseCase(UserCheck):
    def __init__(
        self,
        creature_size_service: CreatureSizeService,
        user_repository: UserRepository,
        creature_size_repository: CreatureSizeRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__size_repository = creature_size_repository
        self.__size_service = creature_size_service

    async def execute(self, command: UpdateCreatureSizeCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__size_repository.is_size_of_id_exist(command.size_id):
            raise DomainError.not_found(
                f"размера существ с id {command.size_id} не существует"
            )
        size = await self.__size_repository.get_size_of_id(command.size_id)
        if command.name is not None:
            if not await self.__size_service.can_create_with_name(command.name):
                raise DomainError.invalid_data(
                    f"не возможно создать размер существа с название {command.name}"
                )
            size.new_name(command.name)
        if command.description is not None:
            size.new_description(command.description)
        await self.__size_repository.save(size)
