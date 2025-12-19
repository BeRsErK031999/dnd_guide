from uuid import uuid4

import pytest
from adapters.repository.sql import SQLWeaponPropertyRepository
from domain import error
from tests.factories import model_factory

st_property = model_factory.weapon_property_model_factory()


async def create_property(db_helper, prop):
    await SQLWeaponPropertyRepository(db_helper).save(prop)


@pytest.mark.asyncio
async def test_create(db_helper):
    await create_property(db_helper, st_property)
    assert await SQLWeaponPropertyRepository(db_helper).id_exists(
        st_property.weapon_property_id
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["name", "new_name"],
        ["description", "new_name"],
        ["base_range", model_factory.length_model_factory(count=40)],
        ["max_range", model_factory.length_model_factory(count=80)],
        ["second_hand_dice", model_factory.dice_model_factory(count=5)],
    ],
    ids=[
        "new_name",
        "new_description",
        "new_base_range",
        "new_max_range",
        "new_second_hand_dice",
    ],
)
async def test_update(db_helper, field, value):
    prop = model_factory.weapon_property_model_factory()
    await create_property(db_helper, prop)
    repo = SQLWeaponPropertyRepository(db_helper)
    assert await repo.id_exists(prop.weapon_property_id)

    setattr(prop, field, value)
    await repo.save(prop)
    updated_property = await repo.get_by_id(prop.weapon_property_id)
    assert getattr(updated_property, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    await create_property(db_helper, st_property)
    repo = SQLWeaponPropertyRepository(db_helper)
    assert await repo.id_exists(st_property.weapon_property_id)

    await repo.delete(st_property.weapon_property_id)
    assert not await repo.id_exists(st_property.weapon_property_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    try:
        await SQLWeaponPropertyRepository(db_helper).delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [["random_name", False], [st_property.name, True]],
    ids=["not_exists", "exists"],
)
async def test_name_exists(db_helper, name, expected):
    await create_property(db_helper, st_property)
    assert await SQLWeaponPropertyRepository(db_helper).name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await create_property(db_helper, st_property)
    repo = SQLWeaponPropertyRepository(db_helper)
    got_property = await repo.get_by_id(st_property.weapon_property_id)
    assert got_property == st_property


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    try:
        await SQLWeaponPropertyRepository(db_helper).get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"search_by_name": "random_name"}, 0],
        [{"search_by_name": st_property.name}, 1],
        [dict(), 1],
    ],
    ids=["not_exists_name", "one_by_name", "all"],
)
async def test_filter(db_helper, filters, count):
    await create_property(db_helper, st_property)
    result = await SQLWeaponPropertyRepository(db_helper).filter(**filters)
    assert len(result) == count
