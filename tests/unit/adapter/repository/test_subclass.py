from copy import deepcopy
from uuid import uuid4

import pytest
from adapters.repository.sql import (
    SQLClassRepository,
    SQLSourceRepository,
    SQLSubclassRepository,
)
from domain import error
from tests.factories import model_factory

st_source = model_factory.source_model_factory()
st_class = model_factory.class_model_factory(source_id=st_source.source_id)
st_class2 = model_factory.class_model_factory(
    source_id=st_source.source_id, name="second_name", class_id=uuid4()
)
st_subclass = model_factory.subclass_model_factory(class_id=st_class.class_id)


async def create_subclass(db_helper, subclass):
    await SQLSourceRepository(db_helper).save(st_source)
    await SQLClassRepository(db_helper).save(st_class)
    await SQLClassRepository(db_helper).save(st_class2)
    await SQLSubclassRepository(db_helper).save(subclass)


@pytest.mark.asyncio
async def test_create(db_helper):
    await create_subclass(db_helper, st_subclass)
    assert await SQLSubclassRepository(db_helper).id_exists(st_subclass.subclass_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["class_id", st_class2.class_id],
        ["name", "new_name"],
        ["name_in_english", "new_name"],
        ["description", "new_name"],
    ],
    ids=["new_class_id", "new_name", "new_name_in_english", "new_description"],
)
async def test_update(db_helper, field, value):
    subclass = deepcopy(st_subclass)
    await create_subclass(db_helper, subclass)
    repo = SQLSubclassRepository(db_helper)
    assert await repo.id_exists(subclass.subclass_id)

    setattr(subclass, field, value)
    await repo.save(subclass)
    updated_subclass = await repo.get_by_id(subclass.subclass_id)
    assert getattr(updated_subclass, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    repo = SQLSubclassRepository(db_helper)
    await create_subclass(db_helper, st_subclass)
    await repo.delete(st_subclass.subclass_id)
    assert not await repo.id_exists(st_subclass.subclass_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    try:
        await SQLSubclassRepository(db_helper).delete(st_subclass.subclass_id)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,expected",
    [
        [{"name": st_subclass.name}, True],
        [{"name": "random_name"}, False],
    ],
    ids=["exists", "not_exists"],
)
async def test_name_exists(db_helper, filters, expected):
    await create_subclass(db_helper, st_subclass)
    assert await SQLSubclassRepository(db_helper).name_exists(**filters) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await create_subclass(db_helper, st_subclass)
    repo = SQLSubclassRepository(db_helper)
    got_subclass = await repo.get_by_id(st_subclass.subclass_id)
    assert got_subclass == st_subclass


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    try:
        await SQLSubclassRepository(db_helper).get_by_id(st_subclass.subclass_id)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"filter_by_class_id": uuid4()}, 0],
        [{"filter_by_class_id": st_class.class_id}, 1],
        [{}, 1],
    ],
    ids=["not_exists", "exists", "all"],
)
async def test_filter(db_helper, filters, count):
    await create_subclass(db_helper, st_subclass)
    result = await SQLSubclassRepository(db_helper).filter(**filters)
    assert len(result) == count
