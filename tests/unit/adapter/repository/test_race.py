from copy import deepcopy
from uuid import uuid4

import pytest
from adapters.repository.sql import SQLRaceRepository, SQLSourceRepository
from domain import error
from domain.creature_size import CreatureSize
from domain.creature_type import CreatureType
from domain.modifier import Modifier
from tests.factories import model_factory

st_source = model_factory.source_model_factory()
st_source2 = model_factory.source_model_factory(source_id=uuid4(), name="second_name")
st_race = model_factory.race_model_factory(source_id=st_source.source_id)


async def create_race(db_helper, race):
    await SQLSourceRepository(db_helper).save(st_source)
    await SQLSourceRepository(db_helper).save(st_source2)
    await SQLRaceRepository(db_helper).save(race)


@pytest.mark.asyncio
async def test_create(db_helper):
    await create_race(db_helper, st_race)
    assert await SQLRaceRepository(db_helper).id_exists(st_race.race_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["name", "new_name"],
        ["description", "new_name"],
        ["name_in_english", "new_name"],
        ["creature_type", CreatureType.FEY.name.lower()],
        ["creature_size", CreatureSize.TINY.name.lower()],
        [
            "speed",
            model_factory.race_speed_model_factory(
                base_speed=model_factory.length_model_factory(count=30),
                description="new_description",
            ),
        ],
        [
            "age",
            model_factory.race_age_model_factory(
                max_age=10, description="new_description"
            ),
        ],
        [
            "increase_modifiers",
            [
                model_factory.race_increase_modifier_model_factory(
                    modifier=Modifier.INTELLECT.name.lower(), bonus=4
                )
            ],
        ],
        ["source_id", st_source2.source_id],
        [
            "features",
            [
                model_factory.race_feature_model_factory(
                    name="new_name", description="new_description"
                )
            ],
        ],
    ],
)
async def test_update(db_helper, field, value):
    race = deepcopy(st_race)
    await create_race(db_helper, race)
    repo = SQLRaceRepository(db_helper)
    assert await repo.id_exists(race.race_id)

    setattr(race, field, value)
    await repo.save(race)
    updated_race = await repo.get_by_id(race.race_id)
    assert getattr(updated_race, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    await create_race(db_helper, st_race)
    repo = SQLRaceRepository(db_helper)
    assert await repo.id_exists(st_race.race_id)

    await repo.delete(st_race.race_id)
    assert not await repo.id_exists(st_race.race_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    try:
        await SQLRaceRepository(db_helper).delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [[st_race.name, True], ["random_name", False]],
    ids=["exists", "not_exists"],
)
async def test_name_exists(db_helper, name, expected):
    await create_race(db_helper, st_race)
    assert await SQLRaceRepository(db_helper).name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await create_race(db_helper, st_race)
    repo = SQLRaceRepository(db_helper)
    assert await repo.id_exists(st_race.race_id)

    got_race = await repo.get_by_id(st_race.race_id)
    assert got_race == st_race


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    try:
        await SQLRaceRepository(db_helper).get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{}, 1],
        [{"search_by_name": st_race.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [{"filter_by_source_ids": [st_race.source_id]}, 1],
        [{"filter_by_source_ids": [uuid4()]}, 0],
    ],
    ids=["all", "name_exists", "name_not_exists", "source_exists", "source_not_exists"],
)
async def test_filter(db_helper, filters, count):
    await create_race(db_helper, st_race)
    result = await SQLRaceRepository(db_helper).filter(**filters)
    assert len(result) == count
