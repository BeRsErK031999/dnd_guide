import pytest
from application.use_case.command.tool import (
    CreateToolUseCase,
    DeleteToolUseCase,
    UpdateToolUseCase,
)
from application.use_case.query.tool import GetToolsUseCase, GetToolUseCase
from domain import error
from domain.tool import ToolService
from domain.tool.tool_type import ToolType
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_tool = model_factory.tool_model_factory()


def tool_service(tool_repository):
    return ToolService(tool_repository)


async def save_user(user_repository, user):
    await user_repository.create(user)


async def save_tool(tool_repository, tool):
    await tool_repository.create(tool)


async def save_class(class_repository, class_):
    await class_repository.create(class_)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_field,checked_field,checked_value",
    [
        [
            {"tool_type": ToolType.HERBALISM_KIT.name.lower()},
            "tool_type",
            ToolType.HERBALISM_KIT.name.lower(),
        ],
        [{"name": "new_name"}, "name", "new_name"],
        [{"description": "new_name"}, "description", "new_name"],
        [
            {"cost": command_factory.coin_command_factory(count=100)},
            "cost",
            model_factory.coins_model_factory(count=100),
        ],
        [
            {"weight": command_factory.weight_command_factory(count=20)},
            "weight",
            model_factory.weight_model_factory(count=20),
        ],
        [
            {
                "utilizes": [
                    command_factory.tool_utilizes_command_factory(
                        action="action", complexity=10
                    )
                ]
            },
            "utilizes",
            [model_factory.tool_utilizes_model_factory(action="action", complexity=10)],
        ],
    ],
    ids=[
        "tool_type",
        "name",
        "description",
        "cost",
        "weight",
        "utilizes",
    ],
)
async def test_create_ok(
    user_repository, tool_repository, create_field, checked_field, checked_value
):
    await save_user(user_repository, st_user)
    use_case = CreateToolUseCase(
        tool_service(tool_repository), user_repository, tool_repository
    )
    result = await use_case.execute(
        command_factory.ToolCommandFactory.create(
            user_id=st_user.user_id, **create_field
        )
    )
    created_tool = await tool_repository.get_by_id(result)
    assert getattr(created_tool, checked_field) == checked_value


@pytest.mark.asyncio
async def test_create_name_exists(user_repository, tool_repository):
    await save_user(user_repository, st_user)
    await save_tool(tool_repository, st_tool)
    use_case = CreateToolUseCase(
        tool_service(tool_repository), user_repository, tool_repository
    )
    try:
        await use_case.execute(
            command_factory.ToolCommandFactory.create(
                user_id=st_user.user_id, name=st_tool.name
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,checked_field,checked_value",
    [
        [
            {"tool_type": ToolType.HERBALISM_KIT.name.lower()},
            "tool_type",
            ToolType.HERBALISM_KIT.name.lower(),
        ],
        [{"name": "new_name"}, "name", "new_name"],
        [{"description": "new_name"}, "description", "new_name"],
        [
            {"cost": command_factory.coin_command_factory(count=100)},
            "cost",
            model_factory.coins_model_factory(count=100),
        ],
        [
            {"weight": command_factory.weight_command_factory(count=20)},
            "weight",
            model_factory.weight_model_factory(count=20),
        ],
        [
            {
                "utilizes": [
                    command_factory.tool_utilizes_command_factory(
                        action="action", complexity=10
                    )
                ]
            },
            "utilizes",
            [model_factory.tool_utilizes_model_factory(action="action", complexity=10)],
        ],
    ],
    ids=[
        "tool_type",
        "name",
        "description",
        "cost",
        "weight",
        "utilizes",
    ],
)
async def test_update_ok(
    user_repository, tool_repository, update_field, checked_field, checked_value
):
    await save_user(user_repository, st_user)
    await save_tool(tool_repository, st_tool)
    use_case = UpdateToolUseCase(
        tool_service(tool_repository), user_repository, tool_repository
    )
    await use_case.execute(
        command_factory.ToolCommandFactory.update(
            user_id=st_user.user_id, tool_id=st_tool.tool_id, **update_field
        )
    )
    updated_tool = await tool_repository.get_by_id(st_tool.tool_id)
    assert getattr(updated_tool, checked_field) == checked_value


@pytest.mark.asyncio
async def test_update_name_exists(user_repository, tool_repository):
    await save_user(user_repository, st_user)
    await save_tool(tool_repository, st_tool)
    exists_tool = model_factory.tool_model_factory(
        tool_id=st_tool.tool_id, name="second_name"
    )
    await save_tool(tool_repository, exists_tool)
    use_case = UpdateToolUseCase(
        tool_service(tool_repository), user_repository, tool_repository
    )
    try:
        await use_case.execute(
            command_factory.ToolCommandFactory.update(
                user_id=st_user.user_id,
                tool_id=st_tool.tool_id,
                name=exists_tool.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_not_exists(user_repository, tool_repository):
    await save_user(user_repository, st_user)
    use_case = UpdateToolUseCase(
        tool_service(tool_repository), user_repository, tool_repository
    )
    try:
        await use_case.execute(
            command_factory.ToolCommandFactory.update(
                user_id=st_user.user_id, tool_id=st_tool.tool_id, name="new_name"
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(user_repository, tool_repository, class_repository):
    await save_user(user_repository, st_user)
    await save_tool(tool_repository, st_tool)
    use_case = DeleteToolUseCase(user_repository, tool_repository, class_repository)
    await use_case.execute(
        command_factory.ToolCommandFactory.delete(
            user_id=st_user.user_id, tool_id=st_tool.tool_id
        )
    )
    assert not await tool_repository.id_exists(st_tool.tool_id)


@pytest.mark.asyncio
async def test_delete_not_exists(user_repository, tool_repository, class_repository):
    await save_user(user_repository, st_user)
    use_case = DeleteToolUseCase(user_repository, tool_repository, class_repository)
    try:
        await use_case.execute(
            command_factory.ToolCommandFactory.delete(
                user_id=st_user.user_id, tool_id=st_tool.tool_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_with_class(user_repository, tool_repository, class_repository):
    await save_user(user_repository, st_user)
    await save_tool(tool_repository, st_tool)
    exists_class = model_factory.class_model_factory(
        proficiencies=model_factory.class_proficiencies_model_factory(
            tools=[st_tool.tool_id]
        )
    )
    await save_class(class_repository, exists_class)
    use_case = DeleteToolUseCase(user_repository, tool_repository, class_repository)
    try:
        await use_case.execute(
            command_factory.ToolCommandFactory.delete(
                user_id=st_user.user_id, tool_id=st_tool.tool_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_tool_ok(tool_repository):
    await save_tool(tool_repository, st_tool)
    use_case = GetToolUseCase(tool_repository)
    result = await use_case.execute(
        query_factory.ToolQueryFactory.query(tool_id=st_tool.tool_id)
    )
    assert result == st_tool


@pytest.mark.asyncio
async def test_get_tool_not_exists(tool_repository):
    use_case = GetToolUseCase(tool_repository)
    try:
        await use_case.execute(
            query_factory.ToolQueryFactory.query(tool_id=st_tool.tool_id)
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"search_by_name": st_tool.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [dict(), 1],
    ],
    ids=["one", "zero", "all"],
)
async def test_get_tools_ok(tool_repository, filters, count):
    await save_tool(tool_repository, st_tool)
    use_case = GetToolsUseCase(tool_repository)
    result = await use_case.execute(query_factory.ToolQueryFactory.queries(**filters))
    assert len(result) == count
