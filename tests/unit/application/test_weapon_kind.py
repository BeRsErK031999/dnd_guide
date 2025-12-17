from uuid import uuid4

import pytest
from application.use_case.command.weapon_kind import (
    CreateWeaponKindUseCase,
    DeleteWeaponKindUseCase,
    UpdateWeaponKindUseCase,
)
from application.use_case.query.weapon_kind import (
    GetWeaponKindsUseCase,
    GetWeaponKindUseCase,
)
from domain import error
from domain.weapon_kind import WeaponKindService
from domain.weapon_kind.weapon_type import WeaponType
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_kind = model_factory.weapon_kind_model_factory()


def kind_service(weapon_kind_repository):
    return WeaponKindService(weapon_kind_repository)


async def save_user(user_repository, user):
    await user_repository.save(user)


async def save_kind(weapon_kind_repository, weapon_kind):
    await weapon_kind_repository.save(weapon_kind)


async def save_weapon(weapon_repository, weapon):
    await weapon_repository.save(weapon)


@pytest.mark.asyncio
async def test_create_ok(user_repository, weapon_kind_repository):
    await save_user(user_repository, st_user)
    use_case = CreateWeaponKindUseCase(
        kind_service(weapon_kind_repository), user_repository, weapon_kind_repository
    )
    result = await use_case.execute(
        command_factory.WeaponKindCommandFactory.create(user_id=st_user.user_id)
    )
    assert await weapon_kind_repository.id_exists(result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,checked_field,checked_value",
    [
        [
            {"weapon_type": WeaponType.SIMPLE_RANGE.name.lower()},
            "weapon_type",
            WeaponType.SIMPLE_RANGE.name.lower(),
        ],
        [{"name": "new_name"}, "name", "new_name"],
        [{"description": "new_name"}, "description", "new_name"],
    ],
    ids=["weapon_type", "name", "description"],
)
async def test_update_ok(
    user_repository, weapon_kind_repository, update_field, checked_field, checked_value
):
    await save_user(user_repository, st_user)
    await save_kind(weapon_kind_repository, st_kind)
    use_case = UpdateWeaponKindUseCase(
        kind_service(weapon_kind_repository),
        user_repository,
        weapon_kind_repository,
    )
    await use_case.execute(
        command_factory.WeaponKindCommandFactory.update(
            user_id=st_user.user_id, kind_id=st_kind.weapon_kind_id, **update_field
        )
    )
    updated_kind = await weapon_kind_repository.get_by_id(st_kind.weapon_kind_id)
    assert getattr(updated_kind, checked_field) == checked_value


@pytest.mark.asyncio
async def test_update_not_exists(user_repository, weapon_kind_repository):
    await save_user(user_repository, st_user)
    use_case = UpdateWeaponKindUseCase(
        kind_service(weapon_kind_repository),
        user_repository,
        weapon_kind_repository,
    )
    try:
        await use_case.execute(
            command_factory.WeaponKindCommandFactory.update(
                user_id=st_user.user_id, kind_id=st_kind.weapon_kind_id, name="new_name"
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(user_repository, weapon_kind_repository, weapon_repository):
    await save_user(user_repository, st_user)
    await save_kind(weapon_kind_repository, st_kind)
    use_case = DeleteWeaponKindUseCase(
        user_repository, weapon_kind_repository, weapon_repository
    )
    await use_case.execute(
        command_factory.WeaponKindCommandFactory.delete(
            user_id=st_user.user_id, kind_id=st_kind.weapon_kind_id
        )
    )
    assert not await weapon_kind_repository.id_exists(st_kind.weapon_kind_id)


@pytest.mark.asyncio
async def test_delete_with_weapon(
    user_repository, weapon_kind_repository, weapon_repository
):
    await save_user(user_repository, st_user)
    await save_kind(weapon_kind_repository, st_kind)
    weapon = model_factory.weapon_model_factory(weapon_kind_id=st_kind.weapon_kind_id)
    await save_weapon(weapon_repository, weapon)
    use_case = DeleteWeaponKindUseCase(
        user_repository, weapon_kind_repository, weapon_repository
    )
    try:
        await use_case.execute(
            command_factory.WeaponKindCommandFactory.delete(
                user_id=st_user.user_id, kind_id=st_kind.weapon_kind_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository, weapon_kind_repository, weapon_repository
):
    await save_user(user_repository, st_user)
    use_case = DeleteWeaponKindUseCase(
        user_repository, weapon_kind_repository, weapon_repository
    )
    try:
        await use_case.execute(
            command_factory.WeaponKindCommandFactory.delete(
                user_id=st_user.user_id, kind_id=st_kind.weapon_kind_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_kind_ok(weapon_kind_repository):
    await save_kind(weapon_kind_repository, st_kind)
    use_case = GetWeaponKindUseCase(weapon_kind_repository)
    result = await use_case.execute(
        query_factory.WeaponKindQueryFactory.query(kind_id=st_kind.weapon_kind_id)
    )
    assert result == st_kind


@pytest.mark.asyncio
async def test_get_kind_not_exists(weapon_kind_repository):
    await save_kind(weapon_kind_repository, st_kind)
    use_case = GetWeaponKindUseCase(weapon_kind_repository)
    try:
        await use_case.execute(
            query_factory.WeaponKindQueryFactory.query(kind_id=uuid4())
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"search_by_name": st_kind.name}, 1],
        [{"search_by_name": st_kind.name, "filter_by_types": st_kind.weapon_type}, 1],
        [dict(), 1],
        [{"search_by_name": "random_name"}, 0],
    ],
    ids=[
        "one_by_name",
        "one_by_name_and_types",
        "all",
        "zero",
    ],
)
async def test_get_kinds_ok(weapon_kind_repository, filters, count):
    await save_kind(weapon_kind_repository, st_kind)
    use_case = GetWeaponKindsUseCase(weapon_kind_repository)
    result = await use_case.execute(
        query_factory.WeaponKindQueryFactory.queries(**filters)
    )
    assert len(result) == count
