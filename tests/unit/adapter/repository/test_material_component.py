from uuid import uuid4

import pytest
from adapters.repository.sql import SQLMaterialComponentRepository
from domain import error
from tests.factories import model_factory

st_material = model_factory.material_component_model_factory()


@pytest.mark.asyncio
async def test_create(db_helper):
    repo = SQLMaterialComponentRepository(db_helper)
    await repo.save(st_material)
    assert await repo.id_exists(material_id=st_material.material_id)


@pytest.mark.asyncio
async def test_update(db_helper):
    repo = SQLMaterialComponentRepository(db_helper)
    material = model_factory.material_component_model_factory()
    await repo.save(material)
    assert await repo.id_exists(material_id=material.material_id)

    material.name = "new_name"
    await repo.save(material)
    updated_material = await repo.get_by_id(material.material_id)
    assert updated_material.name == "new_name"


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    repo = SQLMaterialComponentRepository(db_helper)
    try:
        await repo.delete(st_material.material_id)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete(db_helper):
    repo = SQLMaterialComponentRepository(db_helper)
    material = model_factory.material_component_model_factory()
    await repo.save(material)
    assert await repo.id_exists(material_id=material.material_id)

    await repo.delete(material.material_id)
    assert not await repo.id_exists(material_id=material.material_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [["random_name", False], [st_material.name, True]],
    ids=["not_exists", "exists"],
)
async def test_name_exists(db_helper, name, expected):
    repo = SQLMaterialComponentRepository(db_helper)
    material = model_factory.material_component_model_factory()
    await repo.save(material)
    assert await repo.name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    repo = SQLMaterialComponentRepository(db_helper)
    await repo.save(st_material)
    got_material = await repo.get_by_id(st_material.material_id)
    assert got_material == st_material


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    repo = SQLMaterialComponentRepository(db_helper)
    await repo.save(st_material)
    try:
        await repo.get_by_id(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,count",
    [
        ["random_name", 0],
        [None, 1],
        [st_material.name, 1],
    ],
    ids=["not_exists", "all", "one"],
)
async def test_filter(db_helper, name, count):
    repo = SQLMaterialComponentRepository(db_helper)
    await repo.save(st_material)

    filtered_materials = await repo.filter(search_by_name=name)
    assert len(filtered_materials) == count
