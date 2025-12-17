from copy import deepcopy
from uuid import uuid4

import pytest
from adapters.repository.sql import (
    SQLClassRepository,
    SQLMaterialComponentRepository,
    SQLSourceRepository,
    SQLSpellRepository,
    SQLSubclassRepository,
)
from domain import error
from domain.damage_type import DamageType
from domain.modifier import Modifier
from domain.spell.school import SpellSchool
from tests.factories import model_factory

st_material = model_factory.material_component_model_factory()
st_source = model_factory.source_model_factory()
st_spell = model_factory.spell_model_factory(
    components=model_factory.spell_component_model_factory(
        material=True, materials=[st_material.material_id]
    ),
    source_id=st_source.source_id,
)
st_class = model_factory.class_model_factory(source_id=st_source.source_id)
st_subclass = model_factory.subclass_model_factory(class_id=st_class.class_id)


async def save_spell(db_helper, spell):
    await SQLSourceRepository(db_helper).save(st_source)
    await SQLMaterialComponentRepository(db_helper).save(st_material)
    await SQLClassRepository(db_helper).save(st_class)
    await SQLSubclassRepository(db_helper).save(st_subclass)
    await SQLSpellRepository(db_helper).save(spell)


@pytest.mark.asyncio
async def test_create(db_helper):
    material_repo = SQLMaterialComponentRepository(db_helper)
    source_repo = SQLSourceRepository(db_helper)
    spell_repo = SQLSpellRepository(db_helper)
    await source_repo.save(st_source)
    await material_repo.save(st_material)
    await spell_repo.save(st_spell)
    assert await spell_repo.id_exists(st_spell.spell_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ["class_ids", [st_class.class_id]],
        ["subclass_ids", [st_subclass.subclass_id]],
        ["name", "new_name"],
        ["description", "new_name"],
        ["next_level_description", "new_name"],
        ["level", 2],
        ["school", SpellSchool.DIVINATION.name.lower()],
        ["damage_type", DamageType.COLD.name.lower()],
        ["duration", model_factory.game_time_model_factory(count=1)],
        ["casting_time", model_factory.game_time_model_factory(count=1)],
        ["spell_range", model_factory.length_model_factory(count=30)],
        ["splash", model_factory.length_model_factory(count=3)],
        [
            "components",
            model_factory.spell_component_model_factory(
                verbal=True,
                symbolic=True,
                material=True,
                materials=[st_material.material_id],
            ),
        ],
        ["concentration", True],
        ["ritual", True],
        [
            "saving_throws",
            [Modifier.DEXTERITY.name.lower(), Modifier.WISDOM.name.lower()],
        ],
        ["name_in_english", "new_name"],
    ],
    ids=[
        "new_class_ids",
        "new_subclass_ids",
        "new_name",
        "new_description",
        "new_next_level_description",
        "new_level",
        "new_school",
        "new_damage_type",
        "new_duration",
        "new_casting_time",
        "new_spell_range",
        "new_splash",
        "new_components",
        "new_concentration",
        "new_ritual",
        "new_saving_throws",
        "new_name_in_english",
    ],
)
async def test_update(db_helper, field, value):
    material_repo = SQLMaterialComponentRepository(db_helper)
    source_repo = SQLSourceRepository(db_helper)
    spell_repo = SQLSpellRepository(db_helper)
    class_repo = SQLClassRepository(db_helper)
    subclass_repo = SQLSubclassRepository(db_helper)
    spell = model_factory.spell_model_factory(source_id=st_source.source_id)
    await material_repo.save(st_material)
    await source_repo.save(st_source)
    await class_repo.save(st_class)
    await subclass_repo.save(st_subclass)
    await spell_repo.save(spell)
    assert await spell_repo.id_exists(st_spell.spell_id)

    setattr(spell, field, value)
    await spell_repo.update(spell)
    updated_spell = await spell_repo.get_by_id(spell.spell_id)
    assert getattr(updated_spell, field) == value


@pytest.mark.asyncio
async def test_update_source(db_helper):
    source_repo = SQLSourceRepository(db_helper)
    spell_repo = SQLSpellRepository(db_helper)
    old_source = model_factory.source_model_factory(
        name="old_source", source_id=uuid4()
    )
    new_source = model_factory.source_model_factory(
        name="new_source", source_id=uuid4()
    )
    spell = model_factory.spell_model_factory(source_id=old_source.source_id)
    await source_repo.save(old_source)
    await source_repo.save(new_source)
    await spell_repo.save(spell)
    assert await spell_repo.id_exists(st_spell.spell_id)

    spell.source_id = new_source.source_id
    await spell_repo.update(spell)
    updated_spell = await spell_repo.get_by_id(spell.spell_id)
    assert updated_spell.source_id == new_source.source_id


@pytest.mark.asyncio
async def test_delete(db_helper):
    await save_spell(db_helper, st_spell)
    repo = SQLSpellRepository(db_helper)
    await repo.delete(st_spell.spell_id)
    assert not await repo.id_exists(st_spell.spell_id)


@pytest.mark.asyncio
async def test_delete_not_exists(db_helper):
    repo = SQLSpellRepository(db_helper)
    try:
        await repo.delete(uuid4())
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name,expected",
    [[st_spell.name, True], ["random_name", False]],
    ids=["exists", "not_exists"],
)
async def test_name_exists(db_helper, name, expected):
    await save_spell(db_helper, st_spell)
    repo = SQLSpellRepository(db_helper)
    assert await repo.name_exists(name) == expected


@pytest.mark.asyncio
async def test_get_by_id(db_helper):
    await save_spell(db_helper, st_spell)
    repo = SQLSpellRepository(db_helper)
    spell = await repo.get_by_id(st_spell.spell_id)
    assert spell == st_spell


@pytest.mark.asyncio
async def test_get_by_id_not_exists(db_helper):
    repo = SQLSpellRepository(db_helper)
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
        [{"search_by_name": st_spell.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [{"filter_by_class_ids": [st_class.class_id]}, 1],
        [{"filter_by_class_ids": [uuid4()]}, 0],
        [{"filter_by_subclass_ids": [st_subclass.subclass_id]}, 1],
        [{"filter_by_subclass_ids": [uuid4()]}, 0],
        [{"filter_by_schools": [st_spell.school]}, 1],
        [{"filter_by_schools": ["random_name"]}, 0],
        [{"filter_by_damage_types": [DamageType.COLD.name.lower()]}, 1],
        [{"filter_by_damage_types": ["random_type"]}, 0],
        [{"filter_by_durations": ["random_time"]}, 0],
        [{"filter_by_casting_times": ["random_time"]}, 0],
        [{"filter_by_verbal_component": st_spell.components.verbal}, 1],
        [{"filter_by_verbal_component": not st_spell.components.verbal}, 0],
        [{"filter_by_symbolic_component": st_spell.components.symbolic}, 1],
        [{"filter_by_symbolic_component": not st_spell.components.symbolic}, 0],
        [{"filter_by_material_component": st_spell.components.material}, 1],
        [{"filter_by_material_component": not st_spell.components.material}, 0],
        [{"filter_by_material_ids": st_spell.components.materials}, 1],
        [{"filter_by_material_ids": [uuid4()]}, 0],
        [{"filter_by_concentration": st_spell.concentration}, 1],
        [{"filter_by_concentration": not st_spell.concentration}, 0],
        [{"filter_by_ritual": st_spell.ritual}, 1],
        [{"filter_by_ritual": not st_spell.ritual}, 0],
        [{"filter_by_source_ids": [st_spell.source_id]}, 1],
        [{"filter_by_source_ids": [uuid4()]}, 0],
    ],
    ids=[
        "all",
        "one_search_by_name",
        "zero_search_by_name",
        "one_filter_by_class_ids",
        "zero_filter_by_class_ids",
        "one_filter_by_subclass_ids",
        "zero_filter_by_subclass_ids",
        "one_filter_by_schools",
        "zero_filter_by_schools",
        "one_filter_by_damage_types",
        "zero_filter_by_damage_types",
        "zero_filter_by_durations",
        "zero_filter_by_casting_times",
        "one_filter_by_verbal_component",
        "zero_filter_by_verbal_component",
        "one_filter_by_symbolic_component",
        "zero_filter_by_symbolic_component",
        "one_filter_by_material_component",
        "zero_filter_by_material_component",
        "one_filter_by_material_ids",
        "zero_filter_by_material_ids",
        "one_filter_by_concentration",
        "zero_filter_by_concentration",
        "one_filter_by_ritual",
        "zero_filter_by_ritual",
        "one_filter_by_source_ids",
        "zero_filter_by_source_ids",
    ],
)
async def test_filter(db_helper, filters, count):
    spell = deepcopy(st_spell)
    spell.class_ids = [st_class.class_id]
    spell.subclass_ids = [st_subclass.subclass_id]
    spell.damage_type = DamageType.COLD.name.lower()
    await save_spell(db_helper, spell)
    repo = SQLSpellRepository(db_helper)
    result = await repo.filter(**filters)
    assert len(result) == count
