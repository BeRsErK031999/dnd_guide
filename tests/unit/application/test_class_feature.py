from uuid import uuid4

import pytest
from application.use_case.command.class_feature import (
    CreateClassFeatureUseCase,
    DeleteClassFeatureUseCase,
    UpdateClassFeatureUseCase,
)
from application.use_case.query.class_feature import (
    GetClassFeaturesUseCase,
    GetClassFeatureUseCase,
)
from domain import error
from domain.class_feature import ClassFeatureService
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_class = model_factory.class_model_factory()
st_feature = model_factory.class_feature_model_factory()


def feature_service(feature_repository):
    return ClassFeatureService(feature_repository)


async def save_user(user_repository, user):
    await user_repository.create(user)


async def save_class(class_repository, character_class):
    await class_repository.create(character_class)


async def save_feature(feature_repository, class_feature):
    await feature_repository.create(class_feature)


@pytest.mark.asyncio
async def test_create_ok(user_repository, class_feature_repository, class_repository):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    new_feature = command_factory.ClassFeatureCommandFactory.create(
        user_id=st_user.user_id, class_id=st_class.class_id
    )
    use_case = CreateClassFeatureUseCase(
        feature_service(class_feature_repository),
        user_repository,
        class_repository,
        class_feature_repository,
    )
    result = await use_case.execute(new_feature)
    assert await class_feature_repository.id_exists(result)


@pytest.mark.asyncio
async def test_create_class_not_exists(
    user_repository, class_feature_repository, class_repository
):
    await save_user(user_repository, st_user)
    new_feature = command_factory.ClassFeatureCommandFactory.create(
        user_id=st_user.user_id, class_id=st_class.class_id
    )
    use_case = CreateClassFeatureUseCase(
        feature_service(class_feature_repository),
        user_repository,
        class_repository,
        class_feature_repository,
    )
    try:
        await use_case.execute(new_feature)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,checked",
    [
        [{"class_id": st_class.class_id}, {"class_id": st_class.class_id}],
        [
            {"class_id": st_class.class_id, "name": "random_name"},
            {"class_id": st_class.class_id},
        ],
        [{"name": "new_name"}, {"name": "new_name"}],
        [{"description": "new_name"}, {"description": "new_name"}],
        [{"level": 2}, {"level": 2}],
        [{"name_in_english": "new_name"}, {"name_in_english": "new_name"}],
    ],
    ids=[
        "class_id",
        "class_id_and_name",
        "name",
        "description",
        "level",
        "name_in_english",
    ],
)
async def test_update_ok(
    user_repository, class_feature_repository, class_repository, update_field, checked
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_feature(class_feature_repository, st_feature)
    feature_command = command_factory.ClassFeatureCommandFactory.update(
        user_id=st_user.user_id, feature_id=st_feature.feature_id, **update_field
    )
    use_case = UpdateClassFeatureUseCase(
        feature_service(class_feature_repository),
        user_repository,
        class_repository,
        class_feature_repository,
    )
    await use_case.execute(feature_command)
    updated_feature = await class_feature_repository.get_by_id(st_feature.feature_id)
    assert (
        getattr(updated_feature, list(checked.keys())[0]) == list(checked.values())[0]
    )


@pytest.mark.asyncio
async def test_update_class_not_exists(
    user_repository, class_feature_repository, class_repository
):
    await save_user(user_repository, st_user)
    await save_feature(class_feature_repository, st_feature)
    feature_command = command_factory.ClassFeatureCommandFactory.update(
        user_id=st_user.user_id,
        feature_id=st_feature.feature_id,
        class_id=st_class.class_id,
    )
    use_case = UpdateClassFeatureUseCase(
        feature_service(class_feature_repository),
        user_repository,
        class_repository,
        class_feature_repository,
    )
    try:
        await use_case.execute(feature_command)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_feature_not_exists(
    user_repository, class_feature_repository, class_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_feature(class_feature_repository, st_feature)
    feature_command = command_factory.ClassFeatureCommandFactory.update(
        user_id=st_user.user_id, feature_id=uuid4(), name="random_name"
    )
    use_case = UpdateClassFeatureUseCase(
        feature_service(class_feature_repository),
        user_repository,
        class_repository,
        class_feature_repository,
    )
    try:
        await use_case.execute(feature_command)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(user_repository, class_feature_repository, class_repository):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_feature(class_feature_repository, st_feature)
    feature_command = command_factory.ClassFeatureCommandFactory.delete(
        user_id=st_user.user_id, feature_id=st_feature.feature_id
    )
    use_case = DeleteClassFeatureUseCase(user_repository, class_feature_repository)
    await use_case.execute(feature_command)
    assert not await class_feature_repository.id_exists(st_feature.feature_id)


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository, class_feature_repository, class_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_feature(class_feature_repository, st_feature)
    feature_command = command_factory.ClassFeatureCommandFactory.delete(
        user_id=st_user.user_id, feature_id=uuid4()
    )
    use_case = DeleteClassFeatureUseCase(user_repository, class_feature_repository)
    try:
        await use_case.execute(feature_command)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_feature_ok(class_feature_repository, class_repository):
    await save_class(class_repository, st_class)
    await save_feature(class_feature_repository, st_feature)
    feature_query = query_factory.ClassFeatureQueryFactory.query(
        feature_id=st_feature.feature_id
    )
    use_case = GetClassFeatureUseCase(class_feature_repository)
    result = await use_case.execute(feature_query)
    assert result == st_feature


@pytest.mark.asyncio
async def test_get_feature_not_exists(class_feature_repository, class_repository):
    await save_class(class_repository, st_class)
    await save_feature(class_feature_repository, st_feature)
    feature_query = query_factory.ClassFeatureQueryFactory.query(feature_id=uuid4())
    use_case = GetClassFeatureUseCase(class_feature_repository)
    try:
        result = await use_case.execute(feature_query)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter,count",
    [
        [dict(), 1],
        [{"filter_by_class_id": st_feature.class_id}, 1],
        [{"filter_by_class_id": uuid4()}, 0],
    ],
    ids=["empty", "one", "zero"],
)
async def test_get_features_ok(
    class_feature_repository, class_repository, filter, count
):
    await save_class(class_repository, st_class)
    await save_feature(class_feature_repository, st_feature)
    feature_query = query_factory.ClassFeatureQueryFactory.queries(**filter)
    use_case = GetClassFeaturesUseCase(class_feature_repository)
    result = await use_case.execute(feature_query)
    assert len(result) == count
