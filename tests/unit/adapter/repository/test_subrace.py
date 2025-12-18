from copy import deepcopy
from uuid import uuid4

import pytest
from adapters.repository.sql import (
    SQLRaceRepository,
    SQLSourceRepository,
    SQLSubraceRepository,
)
from domain import error
from domain.modifier import Modifier
from tests.factories import model_factory

st_source = model_factory.source_model_factory()
st_race = model_factory.race_model_factory(source_id=st_source.source_id)
st_race2 = model_factory.race_model_factory(
    source_id=st_source.source_id, name="second_name", race_id=uuid4()
)
st_subrace = model_factory.subrace_model_factory(race_id=st_race.race_id)


async def create_subrace(db_helper, subrace):
    await SQLSourceRepository(db_helper).save(st_source)
    await SQLRaceRepository(db_helper).save(st_race)
    await SQLRaceRepository(db_helper).save(st_race2)
    await SQLSubraceRepository(db_helper).save(subrace)


@pytest.mark.asyncio
async def test_create(db_helper):
    await create_subrace(db_helper, st_subrace)
    assert await SQLSubraceRepository(db_helper).id_exists(st_subrace.subrace_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["race_id", st_race2.race_id],
        ["name", "new_name"],
        ["description", "new_name"],
        ["name_in_english", "new_name"],
        [
            "increase_modifiers",
            [
                model_factory.subrace_increase_modifier_model_factory(
                    modifier=Modifier.INTELLECT.name.lower(), bonus=4
                )
            ],
        ],
        [
            "features",
            [
                model_factory.subrace_feature_model_factory(
                    name="new_name", description="new_description"
                )
            ],
        ],
    ],
    ids=[
        "new_race_id",
        "new_name",
        "new_description",
        "new_name_in_english",
        "new_increase_modifiers",
        "new_features",
    ],
)
async def test_update(db_helper, field, value):
    subrace = deepcopy(st_subrace)
    await create_subrace(db_helper, subrace)
    repo = SQLSubraceRepository(db_helper)
    assert await repo.id_exists(subrace.subrace_id)
    model_factory.subrace_model_factory

    setattr(subrace, field, value)
    await repo.save(subrace)
    updated_subrace = await repo.get_by_id(subrace.subrace_id)
    assert getattr(updated_subrace, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    repo = SQLSubraceRepository(db_helper)
    await create_subrace(db_helper, st_subrace)
    await repo.delete(st_subrace.subrace_id)
    assert not await repo.id_exists(st_subrace.subrace_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    try:
        await SQLSubraceRepository(db_helper).delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [["random_name", False], [st_subrace.name, True]],
    ids=["not_exists", "exists"],
)
async def test_name_exists(db_helper, name, expected):
    await create_subrace(db_helper, st_subrace)
    assert await SQLSubraceRepository(db_helper).name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await create_subrace(db_helper, st_subrace)
    got_subrace = await SQLSubraceRepository(db_helper).get_by_id(st_subrace.subrace_id)
    assert got_subrace == st_subrace


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    try:
        await SQLSubraceRepository(db_helper).get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"search_by_name": "random_name"}, 0],
        [{"search_by_name": st_subrace.name}, 1],
        [dict(), 1],
    ],
    ids=["one", "zero", "all"],
)
async def test_filter(db_helper, filters, count):
    await create_subrace(db_helper, st_subrace)
    result = await SQLSubraceRepository(db_helper).filter(**filters)
    assert len(result) == count
