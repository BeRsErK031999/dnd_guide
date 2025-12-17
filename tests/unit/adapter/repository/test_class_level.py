from copy import deepcopy
from uuid import uuid4

import pytest
from adapters.repository.sql import (
    SQLClassLevelRepository,
    SQLClassRepository,
    SQLSourceRepository,
)
from domain import error
from tests.factories import model_factory

st_source = model_factory.source_model_factory()
st_class = model_factory.class_model_factory(
    source_id=st_source.source_id,
)
st_class2 = model_factory.class_model_factory(
    source_id=st_source.source_id,
    name="second_class",
    class_id=uuid4(),
)
st_level = model_factory.class_level_model_factory(
    class_id=st_class.class_id,
)


async def create_level(db_helper, level):
    await SQLSourceRepository(db_helper).save(st_source)
    await SQLClassRepository(db_helper).save(st_class)
    await SQLClassRepository(db_helper).save(st_class2)
    await SQLClassLevelRepository(db_helper).save(level)


@pytest.mark.asyncio
async def test_create(db_helper):
    await create_level(db_helper, st_level)
    assert await SQLClassLevelRepository(db_helper).id_exists(st_level.class_level_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["class_id", st_class2.class_id],
        ["level", st_level.level + 1],
        [
            "dice",
            model_factory.class_level_dice_model_factory(
                hit_dice=model_factory.dice_model_factory(count=1),
                description="new_description",
            ),
        ],
        ["spell_slots", [1, 1, 1, 1, 1]],
        ["number_cantrips_know", 1],
        ["number_spells_know", 1],
        ["number_arcanums_know", 1],
        [
            "points",
            model_factory.class_level_points_model_factory(
                points=1, description="new_description"
            ),
        ],
        [
            "bonus_damage",
            model_factory.class_level_bonus_damage_model_factory(
                damage=5, description="new_description"
            ),
        ],
        [
            "increase_speed",
            model_factory.class_level_increase_speed_model_factory(
                speed=model_factory.length_model_factory(count=30),
                description="new_description",
            ),
        ],
    ],
    ids=[
        "new_class_id",
        "new_level",
        "new_dice",
        "new_spell_slots",
        "new_number_cantrips_know",
        "new_number_spells_know",
        "new_number_arcanums_know",
        "new_points",
        "new_bonus_damage",
        "new_increase_speed",
    ],
)
async def test_update(db_helper, field, value):
    level = deepcopy(st_level)
    await create_level(db_helper, level)
    repo = SQLClassLevelRepository(db_helper)
    assert await repo.id_exists(level.class_level_id)

    setattr(level, field, value)
    await repo.save(level)
    updated_level = await repo.get_by_id(level.class_level_id)
    assert getattr(updated_level, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    await create_level(db_helper, st_level)
    repo = SQLClassLevelRepository(db_helper)
    await repo.delete(st_level.class_level_id)
    assert not await repo.id_exists(st_level.class_level_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    try:
        await SQLClassLevelRepository(db_helper).delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,expected",
    [
        [{"level": st_level.level, "class_id": st_class.class_id}, True],
        [{"level": st_level.level, "class_id": uuid4()}, False],
    ],
    ids=["exists", "not_exists"],
)
async def test_level_exists(db_helper, filters, expected):
    await create_level(db_helper, st_level)
    repo = SQLClassLevelRepository(db_helper)
    assert await repo.level_of_class_exists(**filters) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await create_level(db_helper, st_level)
    repo = SQLClassLevelRepository(db_helper)
    got_level = await repo.get_by_id(st_level.class_level_id)
    assert got_level == st_level


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    try:
        await SQLClassLevelRepository(db_helper).get_by_id(uuid4())
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
    await create_level(db_helper, st_level)
    repo = SQLClassLevelRepository(db_helper)
    result = await repo.filter(**filters)
    assert len(result) == count
