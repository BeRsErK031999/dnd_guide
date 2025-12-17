from uuid import uuid4

import pytest
from adapters.repository.sql import SQLArmorRepository, SQLMaterialRepository
from domain import error
from domain.armor.armor_type import ArmorType
from domain.modifier import Modifier
from tests.factories import model_factory

st_material = model_factory.material_model_factory()
st_armor = model_factory.armor_model_factory(material_id=st_material.material_id)


async def save_armor(db_helper, armor):
    armor_repo = SQLArmorRepository(db_helper)
    material_repo = SQLMaterialRepository(db_helper)
    await material_repo.save(st_material)
    await armor_repo.save(armor)


@pytest.mark.asyncio
async def test_create(db_helper):
    armor_repo = SQLArmorRepository(db_helper)
    material_repo = SQLMaterialRepository(db_helper)
    await material_repo.save(st_material)
    await armor_repo.save(st_armor)
    assert await armor_repo.id_exists(st_armor.armor_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["name", "new_name"],
        ["description", "new_name"],
        ["armor_type", ArmorType.SHIELD.name.lower()],
        ["strength", 10],
        ["stealth", False],
        [
            "armor_class",
            model_factory.armor_class_model_factory(
                base_class=12,
                modifier=Modifier.CHARISMA.name.lower(),
                max_modifier_bonus=2,
            ),
        ],
        ["weight", model_factory.weight_model_factory(count=20)],
        ["cost", model_factory.coins_model_factory(count=100)],
    ],
    ids=[
        "new_name",
        "new_description",
        "new_armor_type",
        "new_strength",
        "new_stealth",
        "new_armor_class",
        "new_weight",
        "new_cost",
    ],
)
async def test_update(db_helper, field, value):
    armor = model_factory.armor_model_factory(material_id=st_material.material_id)
    repo = SQLArmorRepository(db_helper)
    await save_armor(db_helper, armor)
    assert await repo.id_exists(armor.armor_id)

    setattr(armor, field, value)
    await repo.update(armor)
    updated_armor = await repo.get_by_id(armor.armor_id)
    assert updated_armor == armor
    assert getattr(updated_armor, field) == value


@pytest.mark.asyncio
async def test_new_material(db_helper):
    material_repo = SQLMaterialRepository(db_helper)
    armor_repo = SQLArmorRepository(db_helper)
    old_material = model_factory.material_model_factory()
    new_material = model_factory.material_model_factory(
        material_id=uuid4(), name="new_material"
    )
    armor = model_factory.armor_model_factory(material_id=old_material.material_id)
    await material_repo.save(old_material)
    await material_repo.save(new_material)
    await armor_repo.save(armor)

    armor.material_id = new_material.material_id
    await armor_repo.update(armor)
    updated_armor = await armor_repo.get_by_id(armor.armor_id)
    assert updated_armor.material_id == new_material.material_id


@pytest.mark.asyncio
async def test_delete(db_helper):
    repo = SQLArmorRepository(db_helper)
    await save_armor(db_helper, st_armor)
    await repo.delete(st_armor.armor_id)
    assert not await repo.id_exists(st_armor.armor_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    repo = SQLArmorRepository(db_helper)
    try:
        await repo.delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [["random_name", False], [st_armor.name, True]],
    ids=["not_exists", "exists"],
)
async def test_name_exists(db_helper, name, expected):
    repo = SQLArmorRepository(db_helper)
    await save_armor(db_helper, st_armor)
    assert await repo.name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    repo = SQLArmorRepository(db_helper)
    await save_armor(db_helper, st_armor)
    got_armor = await repo.get_by_id(st_armor.armor_id)
    assert got_armor == st_armor


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    repo = SQLArmorRepository(db_helper)
    await save_armor(db_helper, st_armor)
    try:
        await repo.get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{}, 1],
        [{"search_by_name": "random_name"}, 0],
        [{"search_by_name": st_armor.name}, 1],
        [{"filter_by_armor_types": ["random_type"]}, 0],
        [{"filter_by_armor_types": [st_armor.armor_type]}, 1],
        [{"filter_by_material_ids": [uuid4()]}, 0],
        [{"filter_by_material_ids": [st_material.material_id]}, 1],
    ],
    ids=[
        "all",
        "name_not_exists",
        "name_exists",
        "armor_type_not_exists",
        "armor_type_exists",
        "material_id_not_exists",
        "material_id_exists",
    ],
)
async def test_filter(db_helper, filters, count):
    repo = SQLArmorRepository(db_helper)
    await save_armor(db_helper, st_armor)
    armor_list = await repo.filter(**filters)
    assert len(armor_list) == count
