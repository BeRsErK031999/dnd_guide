from uuid import uuid4

import pytest
from adapters.repository.sql import SQLSourceRepository
from domain import error
from tests.factories import model_factory

st_source = model_factory.source_model_factory()


@pytest.mark.asyncio
async def test_create(db_helper):
    repo = SQLSourceRepository(db_helper)
    await repo.save(st_source)
    assert await repo.id_exists(st_source.source_id)


@pytest.mark.asyncio
async def test_update(db_helper):
    repo = SQLSourceRepository(db_helper)
    source = model_factory.source_model_factory()
    await repo.save(source)
    assert await repo.id_exists(source.source_id)

    source.name = "new_name"
    await repo.save(source)
    updated_source = await repo.get_by_id(source.source_id)
    assert updated_source.name == source.name


@pytest.mark.asyncio
async def test_delete(db_helper):
    repo = SQLSourceRepository(db_helper)
    await repo.save(st_source)
    assert await repo.id_exists(st_source.source_id)

    await repo.delete(st_source.source_id)
    assert not await repo.id_exists(st_source.source_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    repo = SQLSourceRepository(db_helper)
    await repo.save(st_source)
    assert await repo.id_exists(st_source.source_id)

    try:
        await repo.delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    repo = SQLSourceRepository(db_helper)
    await repo.save(st_source)
    assert await repo.id_exists(st_source.source_id)

    source = await repo.get_by_id(st_source.source_id)
    assert source == st_source


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    repo = SQLSourceRepository(db_helper)
    await repo.save(st_source)
    assert await repo.id_exists(st_source.source_id)

    try:
        await repo.get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,count",
    [
        ["random_name", 0],
        [None, 1],
        [st_source.name, 1],
    ],
    ids=["not_exists", "all", "one"],
)
async def test_filter(db_helper, name, count):
    repo = SQLSourceRepository(db_helper)
    await repo.save(st_source)
    assert await repo.name_exists(st_source.name)

    sources = await repo.filter(search_by_name=name)
    assert len(sources) == count
