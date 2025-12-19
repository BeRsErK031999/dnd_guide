from copy import deepcopy
from uuid import uuid4

import pytest
from adapters.repository.sql import (
    SQLMaterialRepository,
    SQLWeaponKindRepository,
    SQLWeaponPropertyRepository,
    SQLWeaponRepository,
)
from domain import error
from domain.damage_type import DamageType
from tests.factories import model_factory

st_kind = model_factory.weapon_kind_model_factory()
st_kind2 = model_factory.weapon_kind_model_factory(
    weapon_kind_id=uuid4(), name="second_name"
)
st_prop = model_factory.weapon_property_model_factory()
st_prop2 = model_factory.weapon_property_model_factory(
    weapon_property_id=uuid4(), name="second_name"
)
st_material = model_factory.material_model_factory()
st_material2 = model_factory.material_model_factory(
    material_id=uuid4(), name="second_name"
)
st_weapon = model_factory.weapon_model_factory(
    weapon_kind_id=st_kind.weapon_kind_id,
    weapon_property_ids=[st_prop.weapon_property_id],
    material_id=st_material.material_id,
)


async def create_weapon(db_helper, weapon):
    await SQLWeaponKindRepository(db_helper).save(st_kind)
    await SQLWeaponKindRepository(db_helper).save(st_kind2)
    await SQLWeaponPropertyRepository(db_helper).save(st_prop)
    await SQLWeaponPropertyRepository(db_helper).save(st_prop2)
    await SQLMaterialRepository(db_helper).save(st_material)
    await SQLMaterialRepository(db_helper).save(st_material2)
    await SQLWeaponRepository(db_helper).save(weapon)


@pytest.mark.asyncio
async def test_create(db_helper):
    await create_weapon(db_helper, st_weapon)
    assert await SQLWeaponRepository(db_helper).id_exists(st_weapon.weapon_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["name", "new_name"],
        ["description", "new_name"],
        ["weapon_kind_id", st_kind2.weapon_kind_id],
        ["cost", model_factory.coins_model_factory(count=40)],
        [
            "damage",
            model_factory.weapon_damage_model_factory(
                dice=model_factory.dice_model_factory(count=3),
                damage_type=DamageType.FORCE.name.lower(),
                bonus_damage=5,
            ),
        ],
        ["weight", model_factory.weight_model_factory(count=40)],
        ["weapon_property_ids", [st_prop2.weapon_property_id]],
        ["material_id", st_material2.material_id],
    ],
    ids=[
        "new_name",
        "new_description",
        "new_weapon_kind_id",
        "new_cost",
        "new_damage",
        "new_weight",
        "new_weapon_property_ids",
        "new_material_id",
    ],
)
async def test_update(db_helper, field, value):
    weapon = deepcopy(st_weapon)
    await create_weapon(db_helper, weapon)
    repo = SQLWeaponRepository(db_helper)
    assert await repo.id_exists(weapon.weapon_id)

    setattr(weapon, field, value)
    await repo.save(weapon)
    updated_weapon = await repo.get_by_id(weapon.weapon_id)
    assert getattr(updated_weapon, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    await create_weapon(db_helper, st_weapon)
    repo = SQLWeaponRepository(db_helper)
    assert await repo.id_exists(st_weapon.weapon_id)

    await repo.delete(st_weapon.weapon_id)
    assert not await repo.id_exists(st_weapon.weapon_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    try:
        await SQLWeaponRepository(db_helper).delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [["random_name", False], [st_weapon.name, True]],
    ids=["not_exists", "exists"],
)
async def test_name_exists(db_helper, name, expected):
    await create_weapon(db_helper, st_weapon)
    assert await SQLWeaponRepository(db_helper).name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await create_weapon(db_helper, st_weapon)
    weapon = await SQLWeaponRepository(db_helper).get_by_id(st_weapon.weapon_id)
    assert weapon == st_weapon


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    try:
        await SQLWeaponRepository(db_helper).get_by_id(uuid4())
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
        [{"search_by_name": st_weapon.name}, 1],
        [{"filter_by_kind_ids": [uuid4()]}, 0],
        [{"filter_by_kind_ids": [st_weapon.weapon_kind_id]}, 1],
        [{"filter_by_damage_types": ["random_type"]}, 0],
        [{"filter_by_damage_types": [st_weapon.damage.damage_type]}, 1],
        [{"filter_by_property_ids": [uuid4()]}, 0],
        [{"filter_by_property_ids": st_weapon.weapon_property_ids}, 1],
        [{"filter_by_material_ids": [uuid4()]}, 0],
        [{"filter_by_material_ids": [st_weapon.material_id]}, 1],
    ],
    ids=[
        "all",
        "not_exists_by_name",
        "one_by_name",
        "not_exists_by_kind_id",
        "one_by_kind_id",
        "not_exists_by_damage_type",
        "one_by_damage_type",
        "not_exists_by_property_id",
        "one_by_property_id",
        "not_exists_by_material_id",
        "one_by_material_id",
    ],
)
async def test_filter(db_helper, filters, count):
    await create_weapon(db_helper, st_weapon)
    result = await SQLWeaponRepository(db_helper).filter(**filters)
    assert len(result) == count
