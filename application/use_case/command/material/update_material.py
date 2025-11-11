from application.dto.command.material import UpdateMaterialCommand
from application.repository import MaterialRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.material import MaterialService


class UpdateMaterialUseCase(UserCheck):
    def __init__(
        self,
        material_service: MaterialService,
        user_repository: UserRepository,
        material_repository: MaterialRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__material_service = material_service
        self.__material_repository = material_repository

    async def execute(self, command: UpdateMaterialCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__material_repository.id_exists(command.material_id):
            raise DomainError.not_found(
                f"материала с id {command.material_id} не существует"
            )
        material = await self.__material_repository.get_by_id(command.material_id)
        if command.name is not None:
            if not await self.__material_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"не возможно переименовать материал на новое {command.name}"
                )
            material.new_name(command.name)
        if command.description is not None:
            material.new_description(command.description)
        await self.__material_repository.update(material)
