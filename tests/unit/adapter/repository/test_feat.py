from uuid import uuid4

import pytest
from adapters.repository.sql import SQLFeatRepository
from domain import error
from domain.armor.armor_type import ArmorType
from domain.modifier import Modifier
from tests.factories import model_factory

st_feat = model_factory.feat_model_factory()


@pytest.mark.asyncio
async def test_create(db_helper):
    repo = SQLFeatRepository(db_helper)
    await repo.save(st_feat)
    assert await repo.id_exists(st_feat.feat_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["name", "new_name"],
        ["description", "new_name"],
        ["caster", not st_feat.caster],
        [
            "required_armor_types",
            [ArmorType.SHIELD.name.lower()],
        ],
        [
            "required_modifiers",
            [model_factory.feat_required_modifier_model_factory(min_value=10)],
        ],
        ["increase_modifiers", [Modifier.DEXTERITY.name.lower()]],
    ],
    ids=[
        "new_name",
        "new_description",
        "new_caster",
        "new_required_armor_types",
        "new_required_modifiers",
        "new_increase_modifiers",
    ],
)
async def test_update(db_helper, field, value):
    repo = SQLFeatRepository(db_helper)
    feat = model_factory.feat_model_factory()
    await repo.save(feat)
    assert await repo.id_exists(feat.feat_id)

    setattr(feat, field, value)
    await repo.save(feat)
    updated_feat = await repo.get_by_id(feat.feat_id)
    assert getattr(updated_feat, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    repo = SQLFeatRepository(db_helper)
    await repo.save(st_feat)
    await repo.delete(st_feat.feat_id)
    assert not await repo.id_exists(st_feat.feat_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    repo = SQLFeatRepository(db_helper)
    try:
        await repo.delete(st_feat.feat_id)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [
        ["random_name", 0],
        [st_feat.name, 1],
    ],
    ids=["not_exists", "exists"],
)
async def test_name_exists(db_helper, name, expected):
    repo = SQLFeatRepository(db_helper)
    await repo.save(st_feat)
    assert await repo.name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    repo = SQLFeatRepository(db_helper)
    await repo.save(st_feat)
    assert await repo.id_exists(st_feat.feat_id)

    feat = await repo.get_by_id(st_feat.feat_id)
    assert feat == st_feat


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    repo = SQLFeatRepository(db_helper)
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
        [{"search_by_name": st_feat.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [{"filter_by_caster": st_feat.caster}, 1],
        [{"filter_by_caster": not st_feat.caster}, 0],
        [{"filter_by_required_armor_types": st_feat.required_armor_types}, 1],
        [{"filter_by_required_armor_types": ["random_type"]}, 0],
        [
            {
                "filter_by_required_modifiers": [
                    m.modifier for m in st_feat.required_modifiers
                ]
            },
            1,
        ],
        [{"filter_by_required_modifiers": ["random_modifier"]}, 0],
        [{"filter_by_increase_modifiers": st_feat.increase_modifiers}, 1],
        [{"filter_by_increase_modifiers": ["random_modifier"]}, 0],
    ],
    ids=[
        "all",
        "name",
        "random_name",
        "caster",
        "random_caster",
        "required_armor_types",
        "random_required_armor_types",
        "required_modifiers",
        "random_required_modifiers",
        "increase_modifiers",
        "random_increase_modifiers",
    ],
)
async def test_filter(db_helper, filters, count):
    repo = SQLFeatRepository(db_helper)
    await repo.save(st_feat)
    result = await repo.filter(**filters)
    assert len(result) == count
