from uuid import uuid4

import pytest
from application.use_case.command.subclass_feature import (
    CreateSubclassFeatureUseCase,
    DeleteSubclassFeatureUseCase,
    UpdateSubclassFeatureUseCase,
)
from application.use_case.query.subclass_feature import (
    GetSubclassFeaturesUseCase,
    GetSubclassFeatureUseCase,
)
from domain import error
from domain.subclass_feature import SubclassFeatureService
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_feature = model_factory.subclass_feature_model_factory()
st_subclass = model_factory.subclass_model_factory()


def feature_service(feature_repository):
    return SubclassFeatureService(feature_repository)


async def save_user(user_repository, user):
    await user_repository.create(user)


async def save_feature(feature_repository, feature):
    await feature_repository.create(feature)


async def save_subclass(subclass_repository, subclass):
    await subclass_repository.create(subclass)


@pytest.mark.asyncio
async def test_create_ok(
    user_repository, subclass_feature_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    await save_subclass(subclass_repository, st_subclass)
    use_case = CreateSubclassFeatureUseCase(
        feature_service(subclass_feature_repository),
        user_repository,
        subclass_repository,
        subclass_feature_repository,
    )
    result = await use_case.execute(
        command_factory.SubclassFeatureCommandFactory.create(
            user_id=st_user.user_id, subclass_id=st_subclass.subclass_id
        )
    )
    assert await subclass_feature_repository.id_exists(result)


@pytest.mark.asyncio
async def test_create_subclass_not_exists(
    user_repository, subclass_feature_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    use_case = CreateSubclassFeatureUseCase(
        feature_service(subclass_feature_repository),
        user_repository,
        subclass_repository,
        subclass_feature_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubclassFeatureCommandFactory.create(
                user_id=st_user.user_id, subclass_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_filed,checked_field,checked_value",
    [
        [{"name": "new_name"}, "name", "new_name"],
        [{"description": "new_name"}, "description", "new_name"],
        [{"level": 2}, "level", 2],
        [{"name_in_english": "new_name"}, "name_in_english", "new_name"],
        [
            {"subclass_id": st_subclass.subclass_id},
            "subclass_id",
            st_subclass.subclass_id,
        ],
    ],
    ids=[
        "name",
        "description",
        "level",
        "name_in_english",
        "subclass_id",
    ],
)
async def test_update_ok(
    user_repository,
    subclass_feature_repository,
    subclass_repository,
    update_filed,
    checked_field,
    checked_value,
):
    await save_user(user_repository, st_user)
    await save_subclass(subclass_repository, st_subclass)
    await save_feature(subclass_feature_repository, st_feature)
    use_case = UpdateSubclassFeatureUseCase(
        feature_service(subclass_feature_repository),
        user_repository,
        subclass_repository,
        subclass_feature_repository,
    )
    await use_case.execute(
        command_factory.SubclassFeatureCommandFactory.update(
            user_id=st_user.user_id, feature_id=st_feature.feature_id, **update_filed
        )
    )
    updated_feature = await subclass_feature_repository.get_by_id(st_feature.feature_id)
    assert getattr(updated_feature, checked_field) == checked_value


@pytest.mark.asyncio
async def test_update_not_exists(
    user_repository, subclass_feature_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    await save_subclass(subclass_repository, st_subclass)
    use_case = UpdateSubclassFeatureUseCase(
        feature_service(subclass_feature_repository),
        user_repository,
        subclass_repository,
        subclass_feature_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubclassFeatureCommandFactory.update(
                user_id=st_user.user_id, feature_id=uuid4(), name="new_name"
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_subclass_not_exists(
    user_repository, subclass_feature_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    await save_feature(subclass_feature_repository, st_feature)
    use_case = UpdateSubclassFeatureUseCase(
        feature_service(subclass_feature_repository),
        user_repository,
        subclass_repository,
        subclass_feature_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubclassFeatureCommandFactory.update(
                user_id=st_user.user_id,
                feature_id=st_feature.feature_id,
                subclass_id=uuid4(),
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(
    user_repository, subclass_feature_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    await save_subclass(subclass_repository, st_subclass)
    await save_feature(subclass_feature_repository, st_feature)
    use_case = DeleteSubclassFeatureUseCase(
        user_repository,
        subclass_feature_repository,
    )
    await use_case.execute(
        command_factory.SubclassFeatureCommandFactory.delete(
            user_id=st_user.user_id, feature_id=st_feature.feature_id
        )
    )
    assert not await subclass_feature_repository.id_exists(st_feature.feature_id)


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository, subclass_feature_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    use_case = DeleteSubclassFeatureUseCase(
        user_repository,
        subclass_feature_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubclassFeatureCommandFactory.delete(
                user_id=st_user.user_id, feature_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_subclass_feature_ok(
    subclass_feature_repository, subclass_repository
):
    await save_subclass(subclass_repository, st_subclass)
    await save_feature(subclass_feature_repository, st_feature)
    use_case = GetSubclassFeatureUseCase(subclass_feature_repository)
    result = await use_case.execute(
        query_factory.SubclassFeatureQueryFactory.query(
            feature_id=st_feature.feature_id
        )
    )
    assert result == st_feature


@pytest.mark.asyncio
async def test_get_subclass_feature_not_exists(
    subclass_feature_repository, subclass_repository
):
    await save_subclass(subclass_repository, st_subclass)
    use_case = GetSubclassFeatureUseCase(subclass_feature_repository)
    try:
        await use_case.execute(
            query_factory.SubclassFeatureQueryFactory.query(feature_id=uuid4())
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"filter_by_subclass_id": st_feature.subclass_id}, 1],
        [{"filter_by_subclass_id": uuid4()}, 0],
        [dict(), 1],
    ],
    ids=["one", "zero", "all"],
)
async def test_get_subclass_features_ok(
    subclass_feature_repository, subclass_repository, filters, count
):
    await save_subclass(subclass_repository, st_subclass)
    await save_feature(subclass_feature_repository, st_feature)
    use_case = GetSubclassFeaturesUseCase(subclass_feature_repository)
    result = await use_case.execute(
        query_factory.SubclassFeatureQueryFactory.queries(**filters)
    )
    assert len(result) == count
