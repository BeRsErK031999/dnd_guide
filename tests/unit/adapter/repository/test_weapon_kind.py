from copy import deepcopy
from uuid import uuid4

import pytest
from adapters.repository.sql import SQLWeaponKindRepository
from domain import error
from domain.weapon_kind.weapon_type import WeaponType
from tests.factories import model_factory

st_kind = model_factory.weapon_kind_model_factory()


async def create_kind(db_helper, kind):
    await SQLWeaponKindRepository(db_helper).save(kind)


@pytest.mark.asyncio
async def test_create(db_helper):
    await create_kind(db_helper, st_kind)
    assert await SQLWeaponKindRepository(db_helper).id_exists(st_kind.weapon_kind_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["name", "new_name"],
        ["description", "new_name"],
        ["weapon_type", WeaponType.SIMPLE_RANGE.name.lower()],
    ],
    ids=["new_name", "new_description", "new_weapon_type"],
)
async def test_update(db_helper, field, value):
    kind = deepcopy(st_kind)
    await create_kind(db_helper, kind)
    repo = SQLWeaponKindRepository(db_helper)
    assert await repo.id_exists(kind.weapon_kind_id)

    setattr(kind, field, value)
    await repo.save(kind)
    updated_kind = await repo.get_by_id(kind.weapon_kind_id)
    assert getattr(updated_kind, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    await create_kind(db_helper, st_kind)
    repo = SQLWeaponKindRepository(db_helper)
    assert await repo.id_exists(st_kind.weapon_kind_id)

    await repo.delete(st_kind.weapon_kind_id)
    assert not await repo.id_exists(st_kind.weapon_kind_id)


@pytest.mark.asyncio
async def test_delete_not_exist(db_helper):
    try:
        await SQLWeaponKindRepository(db_helper).delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [["random_name", False], [st_kind.name, True]],
    ids=["not_exists", "exists"],
)
async def test_name_exists(db_helper, name, expected):
    await create_kind(db_helper, st_kind)
    assert await SQLWeaponKindRepository(db_helper).name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await create_kind(db_helper, st_kind)
    got_kind = await SQLWeaponKindRepository(db_helper).get_by_id(
        st_kind.weapon_kind_id
    )
    assert got_kind == st_kind


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    try:
        await SQLWeaponKindRepository(db_helper).get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [dict(), 1],
        [{"search_by_name": "random_name"}, 0],
        [{"search_by_name": st_kind.name}, 1],
        [{"filter_by_types": [WeaponType.SIMPLE_RANGE.name.lower()]}, 0],
        [{"filter_by_types": [st_kind.weapon_type]}, 1],
    ],
    ids=[
        "all",
        "not_exists_by_name",
        "one_by_name",
        "not_exists_by_type",
        "one_by_type",
    ],
)
async def test_filter(db_helper, filters, count):
    await create_kind(db_helper, st_kind)
    result = await SQLWeaponKindRepository(db_helper).filter(**filters)
    assert len(result) == count
