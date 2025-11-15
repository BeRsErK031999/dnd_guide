from uuid import UUID

from application.dto.command.character_subclass import CreateSubclassCommand
from application.repository import ClassRepository, SubclassRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.character_subclass import CharacterSubclass, SubclassService
from domain.error import DomainError


class CreateSubclassUseCase(UserCheck):
    def __init__(
        self,
        subclass_service: SubclassService,
        user_repository: UserRepository,
        class_repository: ClassRepository,
        subclass_repository: SubclassRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__subclass_service = subclass_service
        self.__class_repository = class_repository
        self.__subclass_repository = subclass_repository

    async def execute(self, command: CreateSubclassCommand) -> UUID:
        await self._user_check(command.user_id)
        if not await self.__subclass_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"подкласс с названием {command.name} уже существует"
            )
        if not await self.__class_repository.id_exists(command.class_id):
            raise DomainError.invalid_data(
                f"класса с id {command.class_id} не существует"
            )
        new_subclass = CharacterSubclass(
            await self.__subclass_repository.next_id(),
            command.class_id,
            command.name,
            command.description,
            command.name_in_english,
        )
        await self.__subclass_repository.create(new_subclass)
        return new_subclass.subclass_id()
