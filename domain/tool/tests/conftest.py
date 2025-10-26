from uuid import uuid4

import pytest
from domain.coin import Coins, PieceType
from domain.tool.tool import Tool
from domain.tool.utilize import Utilize
from domain.weight import Weight, WeightUnit


@pytest.fixture
def gen_uuid():
    return uuid4


@pytest.fixture
def weight(request: pytest.FixtureRequest) -> Weight:
    return Weight(float(request.param), WeightUnit.LB)


@pytest.fixture
def coins(request: pytest.FixtureRequest) -> Coins:
    return Coins(int(request.param), PieceType.GOLD)


@pytest.fixture
def utilizes(request) -> list[Utilize]:
    return [Utilize(utilize[0], utilize[1]) for utilize in request.param]


@pytest.fixture
def tool(gen_uuid, request) -> Tool:
    tool_type, name, description, cost, weight, utilizes = request.param
    cost = Coins(cost, PieceType.GOLD)
    weight = Weight(weight, WeightUnit.LB)
    utilizes = [Utilize(utilize[0], utilize[1]) for utilize in utilizes]
    return Tool(gen_uuid(), tool_type, name, description, cost, weight, utilizes)
