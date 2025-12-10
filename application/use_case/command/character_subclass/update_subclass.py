from application.dto.command.character_subclass import UpdateSubclassCommand
from application.dto.model.character_subclass import AppSubclass
from application.repository import ClassRepository, SubclassRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.character_subclass import SubclassService
from domain.error import DomainError


class UpdateSubclassUseCase(UserCheck):
    def __init__(
        self,
        subclass_service: SubclassService,
        user_repository: UserRepository,
        class_repository: ClassRepository,
        subclass_repository: SubclassRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self._subclass_service = subclass_service
        self._class_repository = class_repository
        self._subclass_repository = subclass_repository

    async def execute(self, command: UpdateSubclassCommand) -> None:
        await self._user_check(command.user_id)
        if not await self._subclass_repository.id_exists(command.subclass_id):
            raise DomainError.not_found(
                f"подкласс с id {command.subclass_id} не существует"
            )
        app_changing_class = await self._subclass_repository.get_by_id(
            command.subclass_id
        )
        changing_class = app_changing_class.to_domain()
        if command.class_id is not None:
            if not await self._class_repository.id_exists(command.class_id):
                raise DomainError.invalid_data(
                    f"класса с id {command.class_id} не существует"
                )
            changing_class.new_class_id(command.class_id)
        if command.name is not None:
            if not await self._subclass_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"подкласс с названием {command.name} уже существует"
                )
            changing_class.new_name(command.name)
        if command.description is not None:
            changing_class.new_description(command.description)
        if command.name_in_english is not None:
            changing_class.new_name_in_english(command.name_in_english)
        await self._subclass_repository.update(AppSubclass.from_domain(changing_class))
