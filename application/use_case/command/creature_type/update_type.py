from application.dto.command.creature_type import UpdateCreatureTypeCommand
from application.repository import CreatureTypeRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.creature_type import CreatureTypeService
from domain.error import DomainError


class UpdateCreatureTypeUseCase(UserCheck):
    def __init__(
        self,
        creature_type_service: CreatureTypeService,
        user_repository: UserRepository,
        creature_type_repository: CreatureTypeRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__type_service = creature_type_service
        self.__type_repository = creature_type_repository

    async def execute(self, command: UpdateCreatureTypeCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__type_repository.id_exists(command.type_id):
            raise DomainError.not_found(
                f"типа существа с id {command.type_id} не существует"
            )
        creature_type = await self.__type_repository.get_by_id(command.type_id)
        if command.name is not None:
            if not await self.__type_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"не возможно переименовать тип существа на новое {command.name}"
                )
            creature_type.new_name(command.name)
        if command.description is not None:
            creature_type.new_description(command.description)
        await self.__type_repository.save(creature_type)
