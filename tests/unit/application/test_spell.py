from os import name
from uuid import uuid4

import pytest
from application.use_case.command.spell import (
    CreateSpellUseCase,
    DeleteSpellUseCase,
    UpdateSpellUseCase,
)
from application.use_case.query.spell import GetSpellsUseCase, GetSpellUseCase
from domain import error
from domain.damage_type import DamageType
from domain.modifier import Modifier
from domain.spell import SpellService
from domain.spell.school import SpellSchool
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_spell = model_factory.spell_model_factory()
st_class = model_factory.class_model_factory()
st_subclass = model_factory.subclass_model_factory()
st_source = model_factory.source_model_factory()
st_m_component = model_factory.material_component_model_factory()


def spell_service(spell_repository):
    return SpellService(spell_repository)


async def save_user(user_repository, user):
    await user_repository.create(user)


async def save_spell(spell_repository, spell):
    await spell_repository.create(spell)


async def save_class(class_repository, character_class):
    await class_repository.create(character_class)


async def save_subclass(subclass_repository, subclass):
    await subclass_repository.create(subclass)


async def save_material_component(material_component_repository, material_component):
    await material_component_repository.create(material_component)


async def save_source(source_repository, source):
    await source_repository.create(source)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_field,checked",
    [
        [{"name": "other_name"}, {"name": "other_name"}],
        [{"description": "other_name"}, {"description": "other_name"}],
        [
            {"next_level_description": "other_name"},
            {"next_level_description": "other_name"},
        ],
        [{"level": 3}, {"level": 3}],
        [
            {"school": SpellSchool.CONJURATION.name.lower()},
            {"school": SpellSchool.CONJURATION.name.lower()},
        ],
        [
            {
                "damage_type": command_factory.spell_damage_type_command_factory(
                    name=DamageType.FIRE.name.lower()
                )
            },
            {"damage_type": DamageType.FIRE.name.lower()},
        ],
        [
            {
                "duration": command_factory.spell_duration_command_factory(
                    command_factory.game_time_command_factory(count=4)
                )
            },
            {"duration": model_factory.game_time_model_factory(count=4)},
        ],
        [
            {"casting_time": command_factory.game_time_command_factory(count=4)},
            {"casting_time": model_factory.game_time_model_factory(count=4)},
        ],
        [
            {"spell_range": command_factory.length_command_factory(count=10)},
            {"spell_range": model_factory.length_model_factory(count=10)},
        ],
        [
            {
                "splash": command_factory.splash_command_factory(
                    command_factory.length_command_factory(count=10)
                )
            },
            {"splash": model_factory.length_model_factory(count=10)},
        ],
        [{"concentration": True}, {"concentration": True}],
        [{"ritual": True}, {"ritual": True}],
        [
            {
                "saving_throws": [
                    Modifier.CONSTITUTION.name.lower(),
                    Modifier.DEXTERITY.name.lower(),
                ]
            },
            {
                "saving_throws": [
                    Modifier.CONSTITUTION.name.lower(),
                    Modifier.DEXTERITY.name.lower(),
                ]
            },
        ],
        [{"name_in_english": "other_name"}, {"name_in_english": "other_name"}],
    ],
    ids=[
        "name",
        "description",
        "next_level_description",
        "level",
        "school",
        "damage_type",
        "duration",
        "casting_time",
        "spell_range",
        "splash",
        "concentration",
        "ritual",
        "saving_throws",
        "name_in_english",
    ],
)
async def test_create_ok(
    spell_repository,
    user_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
    create_field,
    checked,
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    use_case = CreateSpellUseCase(
        spell_service(spell_repository),
        user_repository,
        spell_repository,
        class_repository,
        subclass_repository,
        material_component_repository,
        source_repository,
    )
    result = await use_case.execute(
        command_factory.SpellCommandFactory.create(
            user_id=st_user.user_id,
            class_ids=[st_class.class_id],
            subclass_ids=[st_subclass.subclass_id],
            source_id=st_source.source_id,
            components=command_factory.spell_components_command_factory(
                material=True,
                materials=[st_m_component.material_id],
            ),
            **create_field,
        )
    )
    new_spell = await spell_repository.get_by_id(result)
    assert getattr(new_spell, list(checked.keys())[0]) == list(checked.values())[0]
    assert new_spell.class_ids == [st_class.class_id]
    assert new_spell.subclass_ids == [st_subclass.subclass_id]
    assert new_spell.components.materials == [st_m_component.material_id]
    assert new_spell.source_id == st_source.source_id


@pytest.mark.asyncio
async def test_create_name_exists(
    spell_repository,
    user_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    await save_spell(spell_repository, st_spell)
    use_case = CreateSpellUseCase(
        spell_service(spell_repository),
        user_repository,
        spell_repository,
        class_repository,
        subclass_repository,
        material_component_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.SpellCommandFactory.create(
                user_id=st_user.user_id,
                class_ids=[st_class.class_id],
                subclass_ids=[st_subclass.subclass_id],
                source_id=st_source.source_id,
                name=st_spell.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("did not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "not_exists,expected_status",
    [
        ["class", error.DomainErrorStatus.INVALID_DATA],
        ["subclass", error.DomainErrorStatus.INVALID_DATA],
        ["source", error.DomainErrorStatus.INVALID_DATA],
        ["material", error.DomainErrorStatus.INVALID_DATA],
    ],
    ids=["class", "subclass", "source", "material"],
)
async def test_create_not_exists(
    spell_repository,
    user_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
    not_exists,
    expected_status,
):
    await save_user(user_repository, st_user)
    if not_exists != "class":
        await save_class(class_repository, st_class)
    if not_exists != "subclass":
        await save_subclass(subclass_repository, st_subclass)
    if not_exists != "source":
        await save_source(source_repository, st_source)
    if not_exists != "material":
        await save_material_component(material_component_repository, st_m_component)
    use_case = CreateSpellUseCase(
        spell_service(spell_repository),
        user_repository,
        spell_repository,
        class_repository,
        subclass_repository,
        material_component_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.SpellCommandFactory.create(
                user_id=st_user.user_id,
                class_ids=[st_class.class_id],
                subclass_ids=[st_subclass.subclass_id],
                components=command_factory.spell_components_command_factory(
                    material=True, materials=[st_m_component.material_id]
                ),
                source_id=st_source.source_id,
            )
        )
    except error.DomainError as e:
        assert e.status == expected_status
        return
    pytest.fail("did not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,checked",
    [
        [{"name": "other_name"}, {"name": "other_name"}],
        [{"description": "other_name"}, {"description": "other_name"}],
        [
            {"next_level_description": "other_name"},
            {"next_level_description": "other_name"},
        ],
        [{"level": 3}, {"level": 3}],
        [
            {"school": SpellSchool.CONJURATION.name.lower()},
            {"school": SpellSchool.CONJURATION.name.lower()},
        ],
        [
            {
                "damage_type": command_factory.spell_damage_type_command_factory(
                    name=DamageType.FIRE.name.lower()
                )
            },
            {"damage_type": DamageType.FIRE.name.lower()},
        ],
        [
            {
                "duration": command_factory.spell_duration_command_factory(
                    command_factory.game_time_command_factory(count=4)
                )
            },
            {"duration": model_factory.game_time_model_factory(count=4)},
        ],
        [
            {"casting_time": command_factory.game_time_command_factory(count=4)},
            {"casting_time": model_factory.game_time_model_factory(count=4)},
        ],
        [
            {"spell_range": command_factory.length_command_factory(count=20)},
            {"spell_range": model_factory.length_model_factory(count=20)},
        ],
        [
            {
                "splash": command_factory.splash_command_factory(
                    command_factory.length_command_factory(count=10)
                )
            },
            {"splash": model_factory.length_model_factory(count=10)},
        ],
        [{"concentration": True}, {"concentration": True}],
        [{"ritual": True}, {"ritual": True}],
        [
            {
                "saving_throws": [
                    Modifier.CONSTITUTION.name.lower(),
                    Modifier.DEXTERITY.name.lower(),
                ]
            },
            {
                "saving_throws": [
                    Modifier.CONSTITUTION.name.lower(),
                    Modifier.DEXTERITY.name.lower(),
                ]
            },
        ],
        [{"name_in_english": "other_name"}, {"name_in_english": "other_name"}],
        [
            {
                "components": command_factory.spell_components_command_factory(
                    verbal=False, symbolic=False, material=False, materials=[]
                )
            },
            {
                "components": model_factory.spell_component_model_factory(
                    verbal=False, symbolic=False, material=False, materials=[]
                )
            },
        ],
    ],
    ids=[
        "name",
        "description",
        "next_level_description",
        "level",
        "school",
        "damage_type",
        "duration",
        "casting_time",
        "spell_range",
        "splash",
        "concentration",
        "ritual",
        "saving_throws",
        "name_in_english",
        "components",
    ],
)
async def test_update_ok(
    spell_repository,
    user_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
    update_field,
    checked,
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    update_spell = model_factory.spell_model_factory(
        spell_id=uuid4(),
        class_ids=[st_class.class_id],
        subclass_ids=[st_subclass.subclass_id],
        source_id=st_source.source_id,
        components=model_factory.spell_component_model_factory(
            material=True, materials=[st_m_component.material_id]
        ),
    )
    await save_spell(spell_repository, update_spell)
    use_case = UpdateSpellUseCase(
        spell_service(spell_repository),
        user_repository,
        spell_repository,
        class_repository,
        subclass_repository,
        material_component_repository,
        source_repository,
    )
    await use_case.execute(
        command_factory.SpellCommandFactory.update(
            user_id=st_user.user_id, spell_id=update_spell.spell_id, **update_field
        )
    )
    updated_spell = await spell_repository.get_by_id(update_spell.spell_id)
    assert getattr(updated_spell, list(checked.keys())[0]) == list(checked.values())[0]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,error_status",
    [
        [
            {"spell_id": uuid4(), "name": "random_name"},
            error.DomainErrorStatus.NOT_FOUND,
        ],
        [
            {"spell_id": st_spell.spell_id, "class_ids": [uuid4()]},
            error.DomainErrorStatus.INVALID_DATA,
        ],
        [
            {"spell_id": st_spell.spell_id, "subclass_ids": [uuid4()]},
            error.DomainErrorStatus.INVALID_DATA,
        ],
        [
            {
                "spell_id": st_spell.spell_id,
                "components": command_factory.spell_components_command_factory(
                    material=True, materials=[uuid4()]
                ),
            },
            error.DomainErrorStatus.INVALID_DATA,
        ],
        [
            {"spell_id": st_spell.spell_id, "source_id": uuid4()},
            error.DomainErrorStatus.INVALID_DATA,
        ],
    ],
    ids=[
        "spell",
        "class",
        "subclass",
        "material",
        "source",
    ],
)
async def test_update_not_exists(
    spell_repository,
    user_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
    update_field,
    error_status,
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    await save_spell(spell_repository, st_spell)
    use_case = UpdateSpellUseCase(
        spell_service(spell_repository),
        user_repository,
        spell_repository,
        class_repository,
        subclass_repository,
        material_component_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.SpellCommandFactory.update(
                user_id=st_user.user_id, **update_field
            )
        )
    except error.DomainError as e:
        assert e.status == error_status
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_name_exists(
    spell_repository,
    user_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    await save_spell(spell_repository, st_spell)
    second_spell = model_factory.spell_model_factory(
        spell_id=uuid4(), name="random_name"
    )
    await save_spell(spell_repository, second_spell)
    use_case = UpdateSpellUseCase(
        spell_service(spell_repository),
        user_repository,
        spell_repository,
        class_repository,
        subclass_repository,
        material_component_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.SpellCommandFactory.update(
                user_id=st_user.user_id,
                spell_id=second_spell.spell_id,
                name=st_spell.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(
    spell_repository,
    user_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    await save_spell(spell_repository, st_spell)
    use_case = DeleteSpellUseCase(user_repository, spell_repository)
    await use_case.execute(
        command_factory.SpellCommandFactory.delete(
            user_id=st_user.user_id, spell_id=st_spell.spell_id
        )
    )
    assert not await spell_repository.id_exists(st_spell.spell_id)


@pytest.mark.asyncio
async def test_delete_not_exists(
    spell_repository,
    user_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    use_case = DeleteSpellUseCase(user_repository, spell_repository)
    try:
        await use_case.execute(
            command_factory.SpellCommandFactory.delete(
                user_id=st_user.user_id, spell_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_spell_ok(
    spell_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
):
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    await save_spell(spell_repository, st_spell)
    use_case = GetSpellUseCase(spell_repository)
    result = await use_case.execute(
        query_factory.SpellQueryFactory.query(spell_id=st_spell.spell_id)
    )
    assert result == st_spell


@pytest.mark.asyncio
async def test_get_spell_not_exists(
    spell_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
):
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    use_case = GetSpellUseCase(spell_repository)
    try:
        await use_case.execute(query_factory.SpellQueryFactory.query(spell_id=uuid4()))
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter,count",
    [
        [dict(), 1],
        [{"search_by_name": "random_name"}, 0],
        [{"search_by_name": st_spell.name}, 1],
    ],
    ids=["empty", "zero", "one"],
)
async def test_get_spells_ok(
    spell_repository,
    class_repository,
    subclass_repository,
    source_repository,
    material_component_repository,
    filter,
    count,
):
    await save_class(class_repository, st_class)
    await save_subclass(subclass_repository, st_subclass)
    await save_source(source_repository, st_source)
    await save_material_component(material_component_repository, st_m_component)
    await save_spell(spell_repository, st_spell)
    use_case = GetSpellsUseCase(spell_repository)
    result = await use_case.execute(query_factory.SpellQueryFactory.queries(**filter))
    assert len(result) == count
