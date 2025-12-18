from copy import deepcopy
from uuid import uuid4

import pytest
from adapters.repository.sql import (
    SQLClassRepository,
    SQLSourceRepository,
    SQLSubclassFeatureRepository,
    SQLSubclassRepository,
)
from domain import error
from tests.factories import model_factory

st_source = model_factory.source_model_factory()
st_class = model_factory.class_model_factory(source_id=st_source.source_id)
st_subclass = model_factory.subclass_model_factory(class_id=st_class.class_id)
st_subclass2 = model_factory.subclass_model_factory(
    subclass_id=uuid4(), class_id=st_class.class_id, name="second_subclass"
)
st_feature = model_factory.subclass_feature_model_factory(
    subclass_id=st_subclass.subclass_id
)


async def create_feature(db_helper, feature):
    await SQLSourceRepository(db_helper).save(st_source)
    await SQLClassRepository(db_helper).save(st_class)
    await SQLSubclassRepository(db_helper).save(st_subclass)
    await SQLSubclassRepository(db_helper).save(st_subclass2)
    await SQLSubclassFeatureRepository(db_helper).save(feature)


@pytest.mark.asyncio
async def test_create(db_helper):
    await create_feature(db_helper, st_feature)
    assert await SQLSubclassFeatureRepository(db_helper).id_exists(
        st_feature.feature_id
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["name", "new_name"],
        ["description", "new_name"],
        ["name_in_english", "new_name"],
        ["level", st_feature.level + 1],
        ["subclass_id", st_subclass2.subclass_id],
    ],
    ids=[
        "new_name",
        "new_description",
        "new_name_in_english",
        "new_level",
        "new_subclass_id",
    ],
)
async def test_update(db_helper, field, value):
    feature = deepcopy(st_feature)
    await create_feature(db_helper, feature)
    repo = SQLSubclassFeatureRepository(db_helper)
    assert await repo.id_exists(feature.feature_id)

    setattr(feature, field, value)
    await repo.save(feature)
    updated_feature = await repo.get_by_id(feature.feature_id)
    assert getattr(updated_feature, field) == value


@pytest.mark.asyncio
async def test_delete(db_helper):
    await create_feature(db_helper, st_feature)
    repo = SQLSubclassFeatureRepository(db_helper)
    assert await repo.id_exists(st_feature.feature_id)

    await repo.delete(st_feature.feature_id)
    assert not await repo.id_exists(st_feature.feature_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    try:
        await SQLSubclassFeatureRepository(db_helper).delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,expected",
    [
        [{"subclass_id": st_subclass.subclass_id, "name": st_feature.name}, True],
        [{"subclass_id": st_subclass2.subclass_id, "name": st_feature.name}, False],
    ],
    ids=["exists", "not_exists"],
)
async def test_name_exists(db_helper, filters, expected):
    await create_feature(db_helper, st_feature)
    assert (
        await SQLSubclassFeatureRepository(db_helper).name_for_subclass_exists(
            **filters
        )
        == expected
    )


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await create_feature(db_helper, st_feature)
    repo = SQLSubclassFeatureRepository(db_helper)
    got_feature = await repo.get_by_id(st_feature.feature_id)
    assert got_feature == st_feature


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    try:
        await SQLSubclassFeatureRepository(db_helper).get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"filter_by_subclass_id": st_subclass.subclass_id}, 1],
        [{"filter_by_subclass_id": st_subclass2.subclass_id}, 0],
        [dict(), 1],
    ],
    ids=["one", "zero", "all"],
)
async def test_filter(db_helper, filters, count):
    await create_feature(db_helper, st_feature)
    result = await SQLSubclassFeatureRepository(db_helper).filter(**filters)
    assert len(result) == count
