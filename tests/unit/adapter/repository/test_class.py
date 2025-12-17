from copy import deepcopy
from uuid import uuid4

import pytest
from adapters.repository.sql import (
    SQLClassRepository,
    SQLMaterialRepository,
    SQLToolRepository,
    SQLWeaponKindRepository,
    SQLWeaponPropertyRepository,
    SQLWeaponRepository,
)
from adapters.repository.sql.source import SQLSourceRepository
from domain import error
from domain.modifier import Modifier
from tests.factories import model_factory

st_tool = model_factory.tool_model_factory()
st_tool2 = model_factory.tool_model_factory(tool_id=uuid4(), name="second_tool")
st_weapon_kind = model_factory.weapon_kind_model_factory()
st_weapon_prop = model_factory.weapon_property_model_factory()
st_material = model_factory.material_model_factory()
st_weapon = model_factory.weapon_model_factory(
    weapon_kind_id=st_weapon_kind.weapon_kind_id,
    weapon_property_ids=[st_weapon_prop.weapon_property_id],
    material_id=st_material.material_id,
)
st_weapon2 = model_factory.weapon_model_factory(
    weapon_id=uuid4(),
    weapon_kind_id=st_weapon_kind.weapon_kind_id,
    weapon_property_ids=[st_weapon_prop.weapon_property_id],
    material_id=st_material.material_id,
    name="second_weapon",
)
st_source = model_factory.source_model_factory()
st_source2 = model_factory.source_model_factory(source_id=uuid4(), name="second_source")
st_class = model_factory.class_model_factory(
    source_id=st_source.source_id,
    proficiencies=model_factory.class_proficiencies_model_factory(
        weapons=[st_weapon.weapon_id], tools=[st_tool.tool_id]
    ),
)
st_class2 = model_factory.class_model_factory(
    class_id=uuid4(),
    name="second_class",
    source_id=st_source.source_id,
    proficiencies=model_factory.class_proficiencies_model_factory(
        weapons=[st_weapon.weapon_id], tools=[st_tool.tool_id]
    ),
)


async def save_class(db_helper, class_):
    await SQLToolRepository(db_helper).save(st_tool)
    await SQLToolRepository(db_helper).save(st_tool2)
    await SQLWeaponKindRepository(db_helper).save(st_weapon_kind)
    await SQLWeaponPropertyRepository(db_helper).save(st_weapon_prop)
    await SQLMaterialRepository(db_helper).save(st_material)
    await SQLWeaponRepository(db_helper).save(st_weapon)
    await SQLWeaponRepository(db_helper).save(st_weapon2)
    await SQLSourceRepository(db_helper).save(st_source)
    await SQLSourceRepository(db_helper).save(st_source2)
    await SQLClassRepository(db_helper).save(class_)


@pytest.mark.asyncio
async def test_create(db_helper):
    await save_class(db_helper, st_class)
    repo = SQLClassRepository(db_helper)
    assert await repo.id_exists(st_class.class_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field, value",
    [
        ["name", "new_name"],
        ["description", "new_name"],
        ["primary_modifiers", [Modifier.WISDOM.name.lower()]],
        ["hits", model_factory.class_hits_model_factory(starting_hits=20)],
        [
            "proficiencies",
            model_factory.class_proficiencies_model_factory(
                tools=[st_tool2.tool_id], weapons=[st_weapon2.weapon_id]
            ),
        ],
        ["name_in_english", "new_name"],
        ["source_id", st_source2.source_id],
    ],
    ids=[
        "new_name",
        "new_description",
        "new_primary_modifiers",
        "new_hits",
        "new_proficiencies",
        "new_name_in_english",
        "new_source_id",
    ],
)
async def test_update(db_helper, field, value):
    class_ = deepcopy(st_class)
    await save_class(db_helper, class_)
    repo = SQLClassRepository(db_helper)
    assert await repo.id_exists(class_.class_id)

    setattr(class_, field, value)
    await repo.save(class_)
    updated_class = await repo.get_by_id(class_.class_id)
    assert getattr(updated_class, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    await save_class(db_helper, st_class)
    repo = SQLClassRepository(db_helper)
    assert await repo.id_exists(st_class.class_id)

    await repo.delete(st_class.class_id)
    assert not await repo.id_exists(st_class.class_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    repo = SQLClassRepository(db_helper)
    try:
        await repo.delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [["random_name", False], [st_class.name, True]],
    ids=["not_exists", "exists"],
)
async def test_name_exists(db_helper, name, expected):
    await save_class(db_helper, st_class)
    repo = SQLClassRepository(db_helper)
    assert await repo.name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await save_class(db_helper, st_class)
    repo = SQLClassRepository(db_helper)
    got_class = await repo.get_by_id(st_class.class_id)
    assert got_class == st_class


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    repo = SQLClassRepository(db_helper)
    try:
        await repo.get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters, count",
    [
        [{}, 1],
        [{"search_by_name": "random_name"}, 0],
        [{"search_by_name": st_class.name}, 1],
        [{"filter_by_source_ids": [uuid4()]}, 0],
        [{"filter_by_source_ids": [st_class.source_id]}, 1],
        [{"filter_by_tool_ids": [uuid4()]}, 0],
        [{"filter_by_tool_ids": [st_tool.tool_id]}, 1],
        [{"filter_by_weapon_ids": [uuid4()]}, 0],
        [{"filter_by_weapon_ids": [st_weapon.weapon_id]}, 1],
    ],
    ids=[
        "all",
        "name_not_exists",
        "name_exists",
        "source_not_exists",
        "source_exists",
        "tool_not_exists",
        "tool_exists",
        "weapon_not_exists",
        "weapon_exists",
    ],
)
async def test_filter(db_helper, filters, count):
    await save_class(db_helper, st_class)
    repo = SQLClassRepository(db_helper)
    result = await repo.filter(**filters)
    assert len(result) == count
