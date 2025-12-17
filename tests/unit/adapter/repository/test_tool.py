from uuid import uuid4

import pytest
from adapters.repository.sql import SQLToolRepository
from domain import error
from tests.factories import model_factory

st_tool = model_factory.tool_model_factory()


@pytest.mark.asyncio
async def test_create(db_helper):
    repo = SQLToolRepository(db_helper)
    await repo.save(st_tool)
    assert await repo.id_exists(st_tool.tool_id)


@pytest.mark.asyncio
async def test_update(db_helper):
    repo = SQLToolRepository(db_helper)
    tool = model_factory.tool_model_factory()
    await repo.save(tool)
    assert await repo.id_exists(tool.tool_id)

    tool.name = "new_name"
    tool.utilizes = [model_factory.tool_utilizes_model_factory("new_name")]
    await repo.save(tool)
    updated_tool = await repo.get_by_id(tool.tool_id)
    assert updated_tool.name == tool.name
    assert updated_tool.utilizes == tool.utilizes


@pytest.mark.asyncio
async def test_delete(db_helper):
    repo = SQLToolRepository(db_helper)
    await repo.save(st_tool)
    assert await repo.id_exists(st_tool.tool_id)

    await repo.delete(st_tool.tool_id)
    assert await repo.id_exists(st_tool.tool_id) == False


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    repo = SQLToolRepository(db_helper)
    try:
        await repo.delete(st_tool.tool_id)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    repo = SQLToolRepository(db_helper)
    await repo.save(st_tool)
    assert await repo.id_exists(st_tool.tool_id)

    tool = await repo.get_by_id(st_tool.tool_id)
    assert tool == st_tool


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    repo = SQLToolRepository(db_helper)
    await repo.save(st_tool)
    try:
        await repo.get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,count",
    [["random_name", 0], [None, 1], [st_tool.name, 1]],
    ids=["not_exists", "all", "one"],
)
async def test_filter(db_helper, name, count):
    repo = SQLToolRepository(db_helper)
    await repo.save(st_tool)
    assert await repo.id_exists(st_tool.tool_id)

    tools = await repo.filter(search_by_name=name)
    assert len(tools) == count
