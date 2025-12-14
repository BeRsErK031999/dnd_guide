from uuid import uuid4

import pytest
from application.use_case.command.subrace import (
    CreateSubraceUseCase,
    DeleteSubraceUseCase,
    UpdateSubraceUseCase,
)
from application.use_case.query.subrace import GetSubracesUseCase, GetSubraceUseCase
from domain import error
from domain.modifier import Modifier
from domain.subrace import SubraceService
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_race = model_factory.race_model_factory()
st_subrace = model_factory.subrace_model_factory()


def subrace_service(subrace_repository):
    return SubraceService(subrace_repository)


async def save_user(user_repository, user):
    await user_repository.create(user)


async def save_subrace(subrace_repository, subrace):
    await subrace_repository.create(subrace)


async def save_race(race_repository, race):
    await race_repository.create(race)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_field,checked_field,checked_value",
    [
        [{"name": "new_name"}, "name", "new_name"],
        [{"description": "new_name"}, "description", "new_name"],
        [
            {
                "increase_modifiers": [
                    command_factory.subrace_increase_modifier_command_factory(
                        modifier=Modifier.STRENGTH.name.lower(), bonus=3
                    )
                ]
            },
            "increase_modifiers",
            [
                model_factory.subrace_increase_modifier_model_factory(
                    modifier=Modifier.STRENGTH.name.lower(), bonus=3
                )
            ],
        ],
        [{"name_in_english": "new_name"}, "name_in_english", "new_name"],
        [
            {
                "features": [
                    command_factory.subrace_feature_command_factory(
                        name="name", description="description"
                    )
                ]
            },
            "features",
            [
                model_factory.subrace_feature_model_factory(
                    name="name", description="description"
                )
            ],
        ],
    ],
    ids=[
        "name",
        "description",
        "increase_modifiers",
        "name_in_english",
        "features",
    ],
)
async def test_create_ok(
    user_repository,
    race_repository,
    subrace_repository,
    create_field,
    checked_field,
    checked_value,
):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    use_case = CreateSubraceUseCase(
        subrace_service(subrace_repository),
        user_repository,
        subrace_repository,
        race_repository,
    )
    result = await use_case.execute(
        command_factory.SubraceCommandFactory.create(
            user_id=st_user.user_id, race_id=st_race.race_id, **create_field
        )
    )
    created_subrace = await subrace_repository.get_by_id(result)
    assert getattr(created_subrace, checked_field) == checked_value


@pytest.mark.asyncio
async def test_create_name_exists(user_repository, race_repository, subrace_repository):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    await save_subrace(subrace_repository, st_subrace)
    use_case = CreateSubraceUseCase(
        subrace_service(subrace_repository),
        user_repository,
        subrace_repository,
        race_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubraceCommandFactory.create(
                user_id=st_user.user_id,
                race_id=st_race.race_id,
                name=st_subrace.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_create_race_not_exists(
    user_repository, race_repository, subrace_repository
):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    use_case = CreateSubraceUseCase(
        subrace_service(subrace_repository),
        user_repository,
        subrace_repository,
        race_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubraceCommandFactory.create(
                user_id=st_user.user_id, race_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,checked_field,checked_value",
    [
        [{"name": "new_name"}, "name", "new_name"],
        [{"description": "new_name"}, "description", "new_name"],
        [
            {
                "increase_modifiers": [
                    command_factory.subrace_increase_modifier_command_factory(
                        modifier=Modifier.STRENGTH.name.lower(), bonus=3
                    )
                ]
            },
            "increase_modifiers",
            [
                model_factory.subrace_increase_modifier_model_factory(
                    modifier=Modifier.STRENGTH.name.lower(), bonus=3
                )
            ],
        ],
        [{"name_in_english": "new_name"}, "name_in_english", "new_name"],
        [
            {
                "new_features": [
                    command_factory.subrace_feature_command_factory(
                        name="name", description="description"
                    )
                ]
            },
            "features",
            [
                model_factory.subrace_feature_model_factory(
                    name="name", description="description"
                )
            ],
        ],
        [
            {
                "add_features": [
                    command_factory.subrace_feature_command_factory(
                        name="name", description="description"
                    )
                ]
            },
            "features",
            [
                *st_subrace.features,
                model_factory.subrace_feature_model_factory(
                    name="name", description="description"
                ),
            ],
        ],
        [
            {"remove_features": [f.name for f in st_subrace.features]},
            "features",
            [],
        ],
    ],
    ids=[
        "name",
        "description",
        "increase_modifiers",
        "name_in_english",
        "new_features",
        "add_features",
        "remove_features",
    ],
)
async def test_update_ok(
    user_repository,
    race_repository,
    subrace_repository,
    update_field,
    checked_field,
    checked_value,
):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    await save_subrace(subrace_repository, st_subrace)
    use_case = UpdateSubraceUseCase(
        subrace_service(subrace_repository),
        user_repository,
        subrace_repository,
        race_repository,
    )
    await use_case.execute(
        command_factory.SubraceCommandFactory.update(
            user_id=st_user.user_id, subrace_id=st_subrace.subrace_id, **update_field
        )
    )
    updated_subrace = await subrace_repository.get_by_id(st_subrace.subrace_id)
    assert getattr(updated_subrace, checked_field) == checked_value


@pytest.mark.asyncio
async def test_update_name_exists(user_repository, race_repository, subrace_repository):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    await save_subrace(subrace_repository, st_subrace)
    exists_subrace = model_factory.subrace_model_factory(
        subrace_id=uuid4(), name="second_name"
    )
    await save_subrace(subrace_repository, exists_subrace)
    use_case = UpdateSubraceUseCase(
        subrace_service(subrace_repository),
        user_repository,
        subrace_repository,
        race_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubraceCommandFactory.update(
                user_id=st_user.user_id,
                subrace_id=st_subrace.subrace_id,
                name=exists_subrace.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_subrace_not_exists(
    user_repository, race_repository, subrace_repository
):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    use_case = UpdateSubraceUseCase(
        subrace_service(subrace_repository),
        user_repository,
        subrace_repository,
        race_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubraceCommandFactory.update(
                user_id=st_user.user_id, subrace_id=uuid4(), name="new_name"
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(user_repository, race_repository, subrace_repository):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    await save_subrace(subrace_repository, st_subrace)
    use_case = DeleteSubraceUseCase(
        user_repository,
        subrace_repository,
    )
    await use_case.execute(
        command_factory.SubraceCommandFactory.delete(
            user_id=st_user.user_id, subrace_id=st_subrace.subrace_id
        )
    )
    assert not await subrace_repository.id_exists(st_subrace.subrace_id)


@pytest.mark.asyncio
async def test_delete_subrace_not_exists(
    user_repository, race_repository, subrace_repository
):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    use_case = DeleteSubraceUseCase(
        user_repository,
        subrace_repository,
    )
    try:
        await use_case.execute(
            command_factory.SubraceCommandFactory.delete(
                user_id=st_user.user_id, subrace_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_subrace_ok(user_repository, race_repository, subrace_repository):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    await save_subrace(subrace_repository, st_subrace)
    use_case = GetSubraceUseCase(subrace_repository)
    result = await use_case.execute(
        query_factory.SubraceQueryFactory.query(subrace_id=st_subrace.subrace_id)
    )
    assert result == st_subrace


@pytest.mark.asyncio
async def test_get_subrace_not_exists(
    user_repository, race_repository, subrace_repository
):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    await save_subrace(subrace_repository, st_subrace)
    use_case = GetSubraceUseCase(subrace_repository)
    try:
        await use_case.execute(
            query_factory.SubraceQueryFactory.query(subrace_id=uuid4())
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"search_by_name": st_subrace.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [dict(), 1],
    ],
    ids=[
        "one",
        "zero",
        "all",
    ],
)
async def test_get_subraces_ok(
    user_repository, race_repository, subrace_repository, filters, count
):
    await save_user(user_repository, st_user)
    await save_race(race_repository, st_race)
    await save_subrace(subrace_repository, st_subrace)
    use_case = GetSubracesUseCase(subrace_repository)
    result = await use_case.execute(
        query_factory.SubraceQueryFactory.queries(**filters)
    )
    assert len(result) == count
