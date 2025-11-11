from application.dto.command.tool import CreateToolCommand
from application.repository import ToolRepository, UserRepository
from application.use_case.command.user_check import UserCheck
from domain.coin import Coins, PieceType
from domain.error import DomainError
from domain.tool import Tool, ToolService, ToolType, ToolUtilize
from domain.weight import Weight, WeightUnit


class CreateToolUseCase(UserCheck):
    def __init__(
        self,
        tool_service: ToolService,
        user_repository: UserRepository,
        tool_repository: ToolRepository,
    ) -> None:
        UserCheck.__init__(self, user_repository)
        self.__tool_service = tool_service
        self.__tool_repository = tool_repository

    async def execute(self, command: CreateToolCommand) -> None:
        await self._user_check(command.user_id)
        if not await self.__tool_service.can_create_with_name(command.name):
            raise DomainError.invalid_data(
                f"не возможно создать инструмент с названием {command.name}"
            )
        tool = Tool(
            await self.__tool_repository.next_id(),
            ToolType.from_str(command.tool_type),
            command.name,
            command.description,
            Coins(command.cost.count, PieceType.from_str(command.cost.piece_type)),
            Weight(command.weight.count, WeightUnit.from_str(command.weight.unit)),
            [
                ToolUtilize(utilize.action, utilize.complexity)
                for utilize in command.utilizes
            ],
        )
        await self.__tool_repository.create(tool)
