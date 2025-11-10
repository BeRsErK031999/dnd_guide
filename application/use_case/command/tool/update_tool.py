from application.dto.command.tool import UpdateToolCommand
from application.repository import ToolRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.coin import Coins, PieceType
from domain.error import DomainError
from domain.tool import ToolService, ToolType, ToolUtilize
from domain.weight import Weight, WeightUnit


class UpdateToolUseCase(UserCheck):
    def __init__(
        self,
        tool_service: ToolService,
        user_repository: UserRepository,
        tool_repository: ToolRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__tool_service = tool_service
        self.__tool_repository = tool_repository

    async def execute(self, command: UpdateToolCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__tool_repository.id_exists(command.tool_id):
            raise DomainError.not_found(
                f"инструмент с id {command.tool_id} не существует"
            )
        tool = await self.__tool_repository.get_by_id(command.tool_id)
        if command.tool_type is not None:
            tool.new_tool_type(ToolType.from_str(command.tool_type))
        if command.name is not None:
            if not await self.__tool_service.can_rename_with_name(command.name):
                raise DomainError.invalid_data(
                    f"не возможно переименовать инструмент с названием {command.name}"
                )
            tool.new_name(command.name)
        if command.description is not None:
            tool.new_description(command.description)
        if command.cost is not None:
            tool.new_cost(
                Coins(command.cost.count, PieceType.from_str(command.cost.piece_type))
            )
        if command.weight is not None:
            tool.new_weight(
                Weight(command.weight.count, WeightUnit.from_str(command.weight.unit))
            )
        if command.utilizes is not None:
            tool.new_utilizes(
                [
                    ToolUtilize(utilize.action, utilize.complexity)
                    for utilize in command.utilizes
                ]
            )
        await self.__tool_repository.save(tool)
