from typing import Sequence
from uuid import UUID

from domain.coin import Coins
from domain.error import DomainError
from domain.tool.tool_type import ToolType
from domain.tool.utilize import Utilize
from domain.weight import Weight


class Tool:
    def __init__(
        self,
        tool_id: UUID,
        tool_type: ToolType,
        name: str,
        description: str,
        cost: Coins,
        weight: Weight,
        utilizes: Sequence[Utilize],
    ) -> None:
        self.__validate_name(name)
        self.__validate_description(description)
        self.__validate_utilizes(utilizes)
        self.__name = name
        self.__description = description
        self.__tool_id = tool_id
        self.__tool_type = tool_type
        self.__cost = cost
        self.__weight = weight
        self.__utilizes = list(utilizes)

    def tool_id(self) -> UUID:
        return self.__tool_id

    def name(self) -> str:
        return self.__name

    def description(self) -> str:
        return self.__description

    def tool_type(self) -> ToolType:
        return self.__tool_type

    def cost(self) -> Coins:
        return self.__cost

    def weight(self) -> Weight:
        return self.__weight

    def utilizes(self) -> list[Utilize]:
        return self.__utilizes

    def new_name(self, name: str) -> None:
        if self.__name == name:
            raise DomainError.idempotent(
                "текущее название инструментов идентично новому названию"
            )
        self.__validate_name(name)
        self.__name = name

    def new_description(self, description: str) -> None:
        self.__validate_description(description)
        self.__description = description

    def new_tool_type(self, tool_type: ToolType) -> None:
        if self.__tool_type == tool_type:
            raise DomainError.idempotent("текущий тип инструментов равен новому типу")
        self.__tool_type = tool_type

    def new_cost(self, cost: Coins) -> None:
        if self.__cost == cost:
            raise DomainError.idempotent("текущая цена инструментов ровна новой цене")
        self.__cost = cost

    def new_weight(self, weight: Weight) -> None:
        if self.__weight == weight:
            raise DomainError.idempotent("текущая масса инструментов ровна новой массе")
        self.__weight = weight

    def new_utilizes(self, utilizes: Sequence[Utilize]) -> None:
        self.__validate_utilizes(utilizes)
        self.__utilizes = list(utilizes)

    def __validate_name(self, name: str) -> None:
        if len(name) == 0:
            raise DomainError.invalid_data("название инструментов не может быть пустым")
        if len(name) > 50:
            raise DomainError.invalid_data(
                "название инструментов не может превышать длину в 50 символов"
            )

    def __validate_description(self, description: str) -> None:
        if len(description) == 0:
            raise DomainError.invalid_data("описание инструментов не может быть пустым")

    def __validate_utilizes(self, utilizes: Sequence[Utilize]) -> None:
        if len(utilizes) == 0:
            return
        temp = [utilize.action() for utilize in utilizes]
        if len(temp) != len(set(temp)):
            raise DomainError.invalid_data("действия содержат дубликаты")

    def __str__(self) -> str:
        return self.__name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self.__tool_id == value.__tool_id
        raise NotImplemented
