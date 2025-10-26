import pytest
from domain.error import DomainError
from domain.tool.tool import Tool
from domain.tool.tool_type import ToolType


@pytest.mark.parametrize(
    "tool_type, name, description, coins, weight, utilizes, should_error",
    [
        [
            ToolType.ARTISANS_TOOLS,
            "name",
            "description",
            20,
            1,
            [["action", 15], ["action2", 10]],
            False,
        ],
        [
            ToolType.ARTISANS_TOOLS,
            "",
            "description",
            20,
            1,
            [["action", 15], ["action2", 10]],
            True,
        ],
        [
            ToolType.ARTISANS_TOOLS,
            "name",
            "",
            20,
            1,
            [["action", 15], ["action2", 10]],
            True,
        ],
        [
            ToolType.ARTISANS_TOOLS,
            "name",
            "description",
            20,
            1,
            [["action", 15], ["action", 15]],
            True,
        ],
    ],
    indirect=["coins", "weight", "utilizes"],
)
def test_create(
    gen_uuid, tool_type, name, description, coins, weight, utilizes, should_error
):
    try:
        Tool(gen_uuid(), tool_type, name, description, coins, weight, utilizes)
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("не было вызвано исключение")


@pytest.mark.parametrize(
    "tool, name, should_error",
    [
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            "new_name",
            False,
        ],
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            "name",
            True,
        ],
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            "",
            True,
        ],
    ],
    indirect=["tool"],
)
def test_change_name(tool, name, should_error):
    try:
        tool.new_name(name)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert tool.name() == name


@pytest.mark.parametrize(
    "tool, description, should_error",
    [
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            "new_description",
            False,
        ],
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            "description",
            False,
        ],
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            "",
            True,
        ],
    ],
    indirect=["tool"],
)
def test_change_description(tool, description, should_error):
    try:
        tool.new_description(description)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert tool.description() == description


@pytest.mark.parametrize(
    "tool, tool_type, should_error",
    [
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            ToolType.DISGUISE_KIT,
            False,
        ],
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            ToolType.ARTISANS_TOOLS,
            True,
        ],
    ],
    indirect=["tool"],
)
def test_change_tool_type(tool, tool_type, should_error):
    try:
        tool.new_tool_type(tool_type)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert tool.tool_type() == tool_type


@pytest.mark.parametrize(
    "tool, coins, should_error",
    [
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            25,
            False,
        ],
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            20,
            True,
        ],
    ],
    indirect=["tool", "coins"],
)
def test_change_cost(tool, coins, should_error):
    try:
        tool.new_cost(coins)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert tool.cost() == coins


@pytest.mark.parametrize(
    "tool, weight, should_error",
    [
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            2,
            False,
        ],
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            1,
            True,
        ],
    ],
    indirect=["tool", "weight"],
)
def test_change_weight(tool, weight, should_error):
    try:
        tool.new_weight(weight)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert tool.weight() == weight


@pytest.mark.parametrize(
    "tool, utilizes, should_error",
    [
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            [["action", 12], ["action2", 14]],
            False,
        ],
        [
            [
                ToolType.ARTISANS_TOOLS,
                "name",
                "description",
                20,
                1,
                [["action", 15], ["action2", 10]],
            ],
            [["action", 15], ["action2", 10]],
            True,
        ],
    ],
    indirect=["tool", "utilizes"],
)
def test_change_utilizes(tool, utilizes, should_error):
    try:
        tool.new_utilizes(utilizes)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert tool.utilizes() == utilizes
