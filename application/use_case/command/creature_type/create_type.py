from uuid import UUID

from application.dto.command.creature_type import CreateCreatureTypeCommand
from application.repository import CreatureTypeRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.creature_type import CreatureType, CreatureTypeService
from domain.error import DomainError


class CreateCreatureTypeUseCase(UserCheck):
    def __init__(
        self,
        creature_type_service: CreatureTypeService,
        user_repository: UserRepository,
        creature_type_repository: CreatureTypeRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__type_service = creature_type_service
        self.__type_repository = creature_type_repository

    async def execute(self, command: CreateCreatureTypeCommand) -> UUID:
        await self._user_check(command.user_id)
        if not await self.__type_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"невозможно создать тип существа с названием {command.name}"
            )
        creature_type = CreatureType(
            await self.__type_repository.next_id(), command.name, command.description
        )
        await self.__type_repository.create(creature_type)
        return creature_type.type_id()
