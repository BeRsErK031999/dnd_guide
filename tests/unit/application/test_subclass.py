from uuid import uuid4

import pytest
from application.use_case.command.character_subclass import (
    CreateSubclassUseCase,
    DeleteSubclassUseCase,
    UpdateSubclassUseCase,
)
from application.use_case.query.character_subclass import (
    GetSubclassesUseCase,
    GetSubclassUseCase,
)
from domain import error
from domain.character_subclass.service import SubclassService
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_class = model_factory.class_model_factory()
st_subclass = model_factory.subclass_model_factory()


def subclass_service(subclass_repository):
    return SubclassService(subclass_repository)


async def save_user(user_repository, user):
    await user_repository.save(user)


async def save_class(class_repository, character_class):
    await class_repository.save(character_class)


async def save_subclass(subclass_repository, subclass):
    await subclass_repository.save(subclass)


@pytest.mark.asyncio
async def test_create_ok(user_repository, class_repository, subclass_repository):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    subclass_command = command_factory.SubclassCommandFactory.create(
        class_id=st_class.class_id, user_id=st_user.user_id
    )
    use_case = CreateSubclassUseCase(
        subclass_service(subclass_repository),
        user_repository,
        class_repository,
        subclass_repository,
    )
    result = await use_case.execute(subclass_command)
    subclass = await subclass_repository.get_by_id(result)
    assert subclass is not None


@pytest.mark.asyncio
async def test_create_class_not_exists(
    user_repository, class_repository, subclass_repository
):

    await save_user(user_repository, st_user)
    subclass_command = command_factory.SubclassCommandFactory.create(
        class_id=st_class.class_id, user_id=st_user.user_id
    )
    use_case = CreateSubclassUseCase(
        subclass_service(subclass_repository),
        user_repository,
        class_repository,
        subclass_repository,
    )
    try:
        await use_case.execute(subclass_command)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_create_name_exists(
    user_repository, class_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    subclass_command = command_factory.SubclassCommandFactory.create(
        class_id=st_class.class_id, user_id=st_user.user_id, name=st_subclass.name
    )
    use_case = CreateSubclassUseCase(
        subclass_service(subclass_repository),
        user_repository,
        class_repository,
        subclass_repository,
    )
    try:
        await use_case.execute(subclass_command)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,checked_field",
    [
        [{"name": "new_name"}, {"name": "new_name"}],
        [{"description": "new_name"}, {"description": "new_name"}],
        [{"name_in_english": "new_name"}, {"name_in_english": "new_name"}],
    ],
    ids=[],
)
async def test_update_ok(
    user_repository, class_repository, subclass_repository, update_field, checked_field
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    use_case = UpdateSubclassUseCase(
        subclass_service(subclass_repository),
        user_repository,
        class_repository,
        subclass_repository,
    )
    result = await use_case.execute(
        command_factory.SubclassCommandFactory.update(
            user_id=st_user.user_id, subclass_id=st_subclass.subclass_id, **update_field
        )
    )
    subclass = await subclass_repository.get_by_id(st_subclass.subclass_id)
    assert (
        getattr(subclass, list(checked_field.keys())[0])
        == list(checked_field.values())[0]
    )


@pytest.mark.asyncio
async def test_update_class_ok(user_repository, class_repository, subclass_repository):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    new_class = model_factory.class_model_factory(class_id=uuid4(), name="new_class")
    await save_class(class_repository, new_class)
    use_case = UpdateSubclassUseCase(
        subclass_service(subclass_repository),
        user_repository,
        class_repository,
        subclass_repository,
    )
    result = await use_case.execute(
        command_factory.SubclassCommandFactory.update(
            user_id=st_user.user_id,
            subclass_id=st_subclass.subclass_id,
            class_id=new_class.class_id,
        )
    )
    subclass = await subclass_repository.get_by_id(st_subclass.subclass_id)
    assert subclass.class_id == new_class.class_id


@pytest.mark.asyncio
async def test_update_class_not_exists(
    user_repository, class_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    use_case = UpdateSubclassUseCase(
        subclass_service(subclass_repository),
        user_repository,
        class_repository,
        subclass_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubclassCommandFactory.update(
                user_id=st_user.user_id,
                subclass_id=st_subclass.subclass_id,
                class_id=uuid4(),
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_name_exists(
    user_repository, class_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    new_subclass = model_factory.subclass_model_factory(
        subclass_id=uuid4(), class_id=st_class.class_id, name="random_name"
    )
    await save_subclass(subclass_repository, new_subclass)
    use_case = UpdateSubclassUseCase(
        subclass_service(subclass_repository),
        user_repository,
        class_repository,
        subclass_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubclassCommandFactory.update(
                user_id=st_user.user_id,
                subclass_id=new_subclass.subclass_id,
                name=st_subclass.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(user_repository, class_repository, subclass_repository):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    use_case = DeleteSubclassUseCase(user_repository, subclass_repository)
    await use_case.execute(
        command_factory.SubclassCommandFactory.delete(
            user_id=st_user.user_id, subclass_id=st_subclass.subclass_id
        )
    )


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository, class_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    use_case = DeleteSubclassUseCase(user_repository, subclass_repository)
    try:
        await use_case.execute(
            command_factory.SubclassCommandFactory.delete(
                user_id=st_user.user_id, subclass_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_subclass_ok(user_repository, class_repository, subclass_repository):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    use_case = GetSubclassUseCase(subclass_repository)
    result = await use_case.execute(
        query_factory.SubclassQueryFactory.query(subclass_id=st_subclass.subclass_id)
    )
    assert result == st_subclass


@pytest.mark.asyncio
async def test_get_subclass_not_exists(
    user_repository, class_repository, subclass_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    use_case = GetSubclassUseCase(subclass_repository)
    try:
        await use_case.execute(
            query_factory.SubclassQueryFactory.query(subclass_id=uuid4())
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter,count",
    [
        [dict(), 1],
        [{"filter_by_class_id": st_subclass.class_id}, 1],
        [{"filter_by_class_id": uuid4()}, 0],
    ],
    ids=["empty_filter", "one_with_filter", "zero_with_filter"],
)
async def test_get_subclasses_ok(
    user_repository, class_repository, subclass_repository, filter, count
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    use_case = GetSubclassesUseCase(subclass_repository)
    result = await use_case.execute(
        query_factory.SubclassQueryFactory.queries(**filter)
    )
    assert len(result) == count
