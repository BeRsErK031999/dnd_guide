from uuid import UUID

from application.dto.command.material import CreateMaterialCommand
from application.repository import MaterialRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.material import Material, MaterialService


class CreateMaterialUseCase(UserCheck):
    def __init__(
        self,
        material_service: MaterialService,
        user_repository: UserRepository,
        material_repository: MaterialRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__material_service = material_service
        self.__material_repository = material_repository

    async def execute(self, command: CreateMaterialCommand) -> UUID:
        await self._user_check(command.user_id)
        if not await self.__material_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"невозможно создать материал с названием {command.name}"
            )
        material = Material(
            await self.__material_repository.next_id(),
            command.name,
            command.description,
        )
        await self.__material_repository.create(material)
        return material.material_id()
