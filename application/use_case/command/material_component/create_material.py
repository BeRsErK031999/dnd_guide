from application.dto.command.material_component import CreateMaterialComponentCommand
from application.repository import MaterialComponentRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError
from domain.material_component import MaterialComponent, MaterialComponentService


class CreateMaterialComponentUseCase(UserCheck):
    def __init__(
        self,
        material_service: MaterialComponentService,
        user_repository: UserRepository,
        material_repository: MaterialComponentRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__material_service = material_service
        self.__material_repository = material_repository

    async def execute(self, command: CreateMaterialComponentCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__material_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"невозможно создать материал с названием {command.name}"
            )
        material = MaterialComponent(
            await self.__material_repository.next_id(),
            command.name,
            command.description,
        )
        await self.__material_repository.create(material)
