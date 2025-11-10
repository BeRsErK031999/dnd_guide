from application.dto.command.material_component import DeleteMaterialComponentCommand
from application.repository import MaterialComponentRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.error import DomainError


class DeleteMaterialComponentUseCase(UserCheck):
    def __init__(
        self,
        user_repository: UserRepository,
        material_repository: MaterialComponentRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__material_repository = material_repository

    async def execute(self, command: DeleteMaterialComponentCommand) -> None:
        self.__user_check(command.user_id)
        if not await self.__material_repository.id_exists(command.material_id):
            raise DomainError.not_found(
                f"материала с id {command.material_id} не существует"
            )
        await self.__material_repository.delete(command.material_id)
