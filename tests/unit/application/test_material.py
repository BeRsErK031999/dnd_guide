from uuid import uuid4

import pytest
from application.use_case.command.material import (
    CreateMaterialUseCase,
    DeleteMaterialUseCase,
    UpdateMaterialUseCase,
)
from application.use_case.query.material import GetMaterialsUseCase, GetMaterialUseCase
from domain import error
from domain.material import MaterialService
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_material = model_factory.material_model_factory()


def material_service(material_repository):
    return MaterialService(material_repository)


async def save_user(user_repository, user):
    await user_repository.save(user)


async def save_material(material_repository, material):
    await material_repository.save(material)


async def save_weapon(weapon_repository, weapon):
    await weapon_repository.save(weapon)


async def save_armor(armor_repository, armor):
    await armor_repository.save(armor)


@pytest.mark.asyncio
async def test_create_ok(user_repository, material_repository):
    await save_user(user_repository, st_user)
    use_case = CreateMaterialUseCase(
        material_service(material_repository), user_repository, material_repository
    )
    result = await use_case.execute(
        command_factory.MaterialCommandFactory.create(user_id=st_user.user_id)
    )
    assert await material_repository.id_exists(result)


@pytest.mark.asyncio
async def test_create_name_exists(user_repository, material_repository):
    await save_user(user_repository, st_user)
    exists_material = model_factory.material_model_factory(
        material_id=uuid4(), name="random"
    )
    await save_material(material_repository, exists_material)
    use_case = CreateMaterialUseCase(
        material_service(material_repository), user_repository, material_repository
    )
    try:
        await use_case.execute(
            command_factory.MaterialCommandFactory.create(
                user_id=st_user.user_id, name=exists_material.name
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_ok(user_repository, material_repository):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    use_case = UpdateMaterialUseCase(
        material_service(material_repository), user_repository, material_repository
    )
    await use_case.execute(
        command_factory.MaterialCommandFactory.update(
            user_id=st_user.user_id,
            material_id=st_material.material_id,
            name="new_name",
            description="new_description",
        )
    )
    material = await material_repository.get_by_id(st_material.material_id)
    assert material.name == "new_name" and material.description == "new_description"


@pytest.mark.asyncio
async def test_update_not_exists(user_repository, material_repository):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    use_case = UpdateMaterialUseCase(
        material_service(material_repository), user_repository, material_repository
    )
    try:
        await use_case.execute(
            command_factory.MaterialCommandFactory.update(
                user_id=st_user.user_id, material_id=uuid4(), name="new_name"
            )
        )
    except error.DomainError as e:

        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_name_exists(user_repository, material_repository):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    exists_material = model_factory.material_model_factory(
        material_id=uuid4(), name="random"
    )
    await save_material(material_repository, exists_material)
    use_case = UpdateMaterialUseCase(
        material_service(material_repository), user_repository, material_repository
    )
    try:
        await use_case.execute(
            command_factory.MaterialCommandFactory.update(
                user_id=st_user.user_id,
                material_id=st_material.material_id,
                name=exists_material.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(
    user_repository, material_repository, armor_repository, weapon_repository
):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    use_case = DeleteMaterialUseCase(
        user_repository, material_repository, armor_repository, weapon_repository
    )
    await use_case.execute(
        command_factory.MaterialCommandFactory.delete(
            user_id=st_user.user_id, material_id=st_material.material_id
        )
    )
    assert not await material_repository.id_exists(st_material.material_id)


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository, material_repository, armor_repository, weapon_repository
):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    use_case = DeleteMaterialUseCase(
        user_repository, material_repository, armor_repository, weapon_repository
    )
    try:
        await use_case.execute(
            command_factory.MaterialCommandFactory.delete(
                user_id=st_user.user_id, material_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_with_armor(
    user_repository, material_repository, armor_repository, weapon_repository
):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    armor = model_factory.armor_model_factory(material_id=st_material.material_id)
    await save_armor(armor_repository, armor)
    use_case = DeleteMaterialUseCase(
        user_repository, material_repository, armor_repository, weapon_repository
    )
    try:
        await use_case.execute(
            command_factory.MaterialCommandFactory.delete(
                user_id=st_user.user_id, material_id=st_material.material_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_with_weapon(
    user_repository, material_repository, armor_repository, weapon_repository
):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    weapon = model_factory.weapon_model_factory(material_id=st_material.material_id)
    await save_weapon(weapon_repository, weapon)
    use_case = DeleteMaterialUseCase(
        user_repository, material_repository, armor_repository, weapon_repository
    )
    try:
        await use_case.execute(
            command_factory.MaterialCommandFactory.delete(
                user_id=st_user.user_id, material_id=st_material.material_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_material_ok(user_repository, material_repository):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    use_case = GetMaterialUseCase(material_repository)
    result = await use_case.execute(
        query_factory.MaterialQueryFactory.query(material_id=st_material.material_id)
    )
    assert result == st_material


@pytest.mark.asyncio
async def test_get_material_not_exists(user_repository, material_repository):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    use_case = GetMaterialUseCase(material_repository)
    try:
        await use_case.execute(
            query_factory.MaterialQueryFactory.query(material_id=uuid4())
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"search_by_name": st_material.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [dict(), 1],
    ],
    ids=["one", "zero", "all"],
)
async def test_get_materials_ok(user_repository, material_repository, filters, count):
    await save_user(user_repository, st_user)
    await save_material(material_repository, st_material)
    use_case = GetMaterialsUseCase(material_repository)
    result = await use_case.execute(
        query_factory.MaterialQueryFactory.queries(**filters)
    )
    assert len(result) == count
