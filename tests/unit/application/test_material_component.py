from uuid import uuid4

import pytest
from application.use_case.command.material_component import (
    CreateMaterialComponentUseCase,
    DeleteMaterialComponentUseCase,
    UpdateMaterialComponentUseCase,
)
from application.use_case.query.material_component import (
    GetMaterialComponentsUseCase,
    GetMaterialComponentUseCase,
)
from domain import error
from domain.material_component import MaterialComponentService
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_material = model_factory.material_component_model_factory()
st_spell = model_factory.spell_model_factory()


def material_component_service(material_component_repository):
    return MaterialComponentService(material_component_repository)


async def save_user(user_repository, user):
    await user_repository.save(user)


async def save_material_component(material_component_repository, material_component):
    await material_component_repository.save(material_component)


async def save_spell(spell_repository, spell):
    await spell_repository.save(spell)


@pytest.mark.asyncio
async def test_create_ok(user_repository, material_component_repository):
    await save_user(user_repository, st_user)
    use_case = CreateMaterialComponentUseCase(
        material_component_service(material_component_repository),
        user_repository,
        material_component_repository,
    )
    result = await use_case.execute(
        command_factory.MaterialComponentCommandFactory.create(user_id=st_user.user_id)
    )
    assert await material_component_repository.id_exists(result)


@pytest.mark.asyncio
async def test_create_name_exists(user_repository, material_component_repository):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    use_case = CreateMaterialComponentUseCase(
        material_component_service(material_component_repository),
        user_repository,
        material_component_repository,
    )
    try:
        await use_case.execute(
            command_factory.MaterialComponentCommandFactory.create(
                user_id=st_user.user_id, name=st_material.name
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,checked",
    [
        [{"name": "new_name"}, {"name": "new_name"}],
        [{"description": "new_name"}, {"description": "new_name"}],
    ],
    ids=["name", "description"],
)
async def test_update_ok(
    user_repository, material_component_repository, update_field, checked
):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    use_case = UpdateMaterialComponentUseCase(
        material_component_service(material_component_repository),
        user_repository,
        material_component_repository,
    )
    await use_case.execute(
        command_factory.MaterialComponentCommandFactory.update(
            user_id=st_user.user_id, material_id=st_material.material_id, **update_field
        )
    )
    updated_material = await material_component_repository.get_by_id(
        st_material.material_id
    )
    assert (
        getattr(updated_material, list(checked.keys())[0]) == list(checked.values())[0]
    )


@pytest.mark.asyncio
async def test_update_not_exists(user_repository, material_component_repository):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    use_case = UpdateMaterialComponentUseCase(
        material_component_service(material_component_repository),
        user_repository,
        material_component_repository,
    )
    try:
        await use_case.execute(
            command_factory.MaterialComponentCommandFactory.update(
                user_id=st_user.user_id, material_id=uuid4(), name="new_name"
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_name_exists(user_repository, material_component_repository):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    exists_material = model_factory.material_component_model_factory(
        material_id=uuid4(), name="second_name"
    )
    await save_material_component(material_component_repository, exists_material)
    use_case = UpdateMaterialComponentUseCase(
        material_component_service(material_component_repository),
        user_repository,
        material_component_repository,
    )
    try:
        await use_case.execute(
            command_factory.MaterialComponentCommandFactory.update(
                user_id=st_user.user_id,
                material_id=exists_material.material_id,
                name=st_material.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(
    user_repository, material_component_repository, spell_repository
):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    use_case = DeleteMaterialComponentUseCase(
        user_repository, material_component_repository, spell_repository
    )
    await use_case.execute(
        command_factory.MaterialComponentCommandFactory.delete(
            user_id=st_user.user_id, material_id=st_material.material_id
        )
    )
    assert not await material_component_repository.id_exists(st_material.material_id)


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository, material_component_repository, spell_repository
):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    use_case = DeleteMaterialComponentUseCase(
        user_repository, material_component_repository, spell_repository
    )
    try:
        await use_case.execute(
            command_factory.MaterialComponentCommandFactory.delete(
                user_id=st_user.user_id, material_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_with_spell(
    user_repository, material_component_repository, spell_repository
):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    spell = model_factory.spell_model_factory(
        components=model_factory.spell_component_model_factory(
            material=True, materials=[st_material.material_id]
        )
    )
    await save_spell(spell_repository, spell)
    use_case = DeleteMaterialComponentUseCase(
        user_repository, material_component_repository, spell_repository
    )
    try:
        await use_case.execute(
            command_factory.MaterialComponentCommandFactory.delete(
                user_id=st_user.user_id, material_id=st_material.material_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_material_ok(user_repository, material_component_repository):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    use_case = GetMaterialComponentUseCase(material_component_repository)
    result = await use_case.execute(
        query_factory.MaterialComponentQueryFactory.query(
            material_id=st_material.material_id
        )
    )
    assert result == st_material


@pytest.mark.asyncio
async def test_get_material_not_exists(user_repository, material_component_repository):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    use_case = GetMaterialComponentUseCase(material_component_repository)
    try:
        await use_case.execute(
            query_factory.MaterialComponentQueryFactory.query(material_id=uuid4())
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
async def test_get_materials_ok(
    user_repository, material_component_repository, filters, count
):
    await save_user(user_repository, st_user)
    await save_material_component(material_component_repository, st_material)
    use_case = GetMaterialComponentsUseCase(material_component_repository)
    result = await use_case.execute(
        query_factory.MaterialComponentQueryFactory.queries(**filters)
    )
    assert len(result) == count
