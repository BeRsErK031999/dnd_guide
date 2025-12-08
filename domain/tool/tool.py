from typing import Sequence
from uuid import UUID

from domain.coin import Coins
from domain.error import DomainError
from domain.mixin import EntityDescription, EntityName
from domain.tool.tool_type import ToolType
from domain.tool.utilize import ToolUtilize
from domain.weight import Weight


class Tool(EntityName, EntityDescription):
    def __init__(
        self,
        tool_id: UUID,
        tool_type: ToolType,
        name: str,
        description: str,
        cost: Coins,
        weight: Weight,
        utilizes: Sequence[ToolUtilize],
    ) -> None:
        self._validate_utilizes(utilizes)
        EntityName.__init__(self, name)
        EntityDescription.__init__(self, description)
        self._tool_id = tool_id
        self._tool_type = tool_type
        self._cost = cost
        self._weight = weight
        self._utilizes = list(utilizes)

    def tool_id(self) -> UUID:
        return self._tool_id

    def tool_type(self) -> ToolType:
        return self._tool_type

    def cost(self) -> Coins:
        return self._cost

    def weight(self) -> Weight:
        return self._weight

    def utilizes(self) -> list[ToolUtilize]:
        return self._utilizes

    def new_tool_type(self, tool_type: ToolType) -> None:
        if self._tool_type == tool_type:
            raise DomainError.idempotent("текущий тип инструментов равен новому типу")
        self._tool_type = tool_type

    def new_cost(self, cost: Coins) -> None:
        if self._cost == cost:
            raise DomainError.idempotent("текущая цена инструментов ровна новой цене")
        self._cost = cost

    def new_weight(self, weight: Weight) -> None:
        if self._weight == weight:
            raise DomainError.idempotent("текущая масса инструментов ровна новой массе")
        self._weight = weight

    def new_utilizes(self, utilizes: Sequence[ToolUtilize]) -> None:
        self._validate_utilizes(utilizes)
        self._utilizes = list(utilizes)

    def _validate_utilizes(self, utilizes: Sequence[ToolUtilize]) -> None:
        if len(utilizes) == 0:
            return
        temp = [utilize.action() for utilize in utilizes]
        if len(temp) != len(set(temp)):
            raise DomainError.invalid_data("действия содержат дубликаты")

    def __str__(self) -> str:
        return self._name

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return self._tool_id == value._tool_id
        if isinstance(value, UUID):
            return self._tool_id == value
        raise NotImplemented
