from uuid import uuid4

import pytest
from application.use_case.command.character_class import (
    CreateClassUseCase,
    DeleteClassUseCase,
    UpdateClassUseCase,
)
from application.use_case.query.character_class import (
    GetClassesUseCase,
    GetClassUseCase,
)
from domain import error
from domain.character_class.service import ClassService
from domain.modifier import Modifier
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_class = model_factory.class_model_factory()
st_tool = model_factory.tool_model_factory()
st_weapon = model_factory.weapon_model_factory()
st_source = model_factory.source_model_factory()


def class_service(class_repository):
    return ClassService(class_repository)


async def save_user(user_repository, user):
    await user_repository.save(user)


async def save_weapon(weapon_repository, weapon):
    await weapon_repository.save(weapon)


async def save_class(class_repository, character_class):
    await class_repository.save(character_class)


async def save_tool(tool_repository, tool):
    await tool_repository.save(tool)


async def save_source(source_repository, source):
    await source_repository.save(source)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command",
    [
        command_factory.ClassCommandFactory.create(
            user_id=st_user.user_id,
            source_id=st_source.source_id,
            proficiencies=command_factory.class_proficiencies_command_factory(
                weapons=[st_weapon.weapon_id], tools=[st_tool.tool_id]
            ),
        ),
        command_factory.ClassCommandFactory.create(
            user_id=st_user.user_id,
            source_id=st_source.source_id,
            proficiencies=command_factory.class_proficiencies_command_factory(
                tools=[st_tool.tool_id],
            ),
        ),
        command_factory.ClassCommandFactory.create(
            user_id=st_user.user_id,
            source_id=st_source.source_id,
            proficiencies=command_factory.class_proficiencies_command_factory(
                weapons=[st_weapon.weapon_id], number_tools=0
            ),
        ),
    ],
    ids=["full", "empty_weapon", "empty_tool"],
)
async def test_create_ok(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
    command,
):
    await save_user(user_repository, st_user)
    await save_weapon(weapon_repository, st_weapon)
    await save_tool(tool_repository, st_tool)
    await save_source(source_repository, st_source)
    use_case = CreateClassUseCase(
        class_service(class_repository),
        user_repository,
        class_repository,
        weapon_repository,
        tool_repository,
        source_repository,
    )
    result = await use_case.execute(command)
    assert result is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field",
    ["weapon", "tool", "source"],
    ids=["weapon", "tool", "source"],
)
async def test_create_not_exists(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
    field,
):
    await save_user(user_repository, st_user)
    if field != "weapon":
        await save_weapon(weapon_repository, st_weapon)
    if field != "tool":
        await save_tool(tool_repository, st_tool)
    if field != "source":
        await save_source(source_repository, st_source)
    use_case = CreateClassUseCase(
        class_service(class_repository),
        user_repository,
        class_repository,
        weapon_repository,
        tool_repository,
        source_repository,
    )
    try:
        result = await use_case.execute(
            command_factory.ClassCommandFactory.create(
                user_id=st_user.user_id,
                source_id=st_source.source_id,
                proficiencies=command_factory.class_proficiencies_command_factory(
                    weapons=[st_weapon.weapon_id], tools=[st_tool.tool_id]
                ),
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_create_name_exists(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon(weapon_repository, st_weapon)
    await save_tool(tool_repository, st_tool)
    await save_source(source_repository, st_source)
    await save_class(class_repository, st_class)
    use_case = CreateClassUseCase(
        class_service(class_repository),
        user_repository,
        class_repository,
        weapon_repository,
        tool_repository,
        source_repository,
    )
    try:
        result = await use_case.execute(
            command_factory.ClassCommandFactory.create(
                user_id=st_user.user_id,
                source_id=st_source.source_id,
                name=st_class.name,
                proficiencies=command_factory.class_proficiencies_command_factory(
                    weapons=[st_weapon.weapon_id], tools=[st_tool.tool_id]
                ),
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field",
    [
        {"name": "new_name", "checked": "new_name"},
        {"description": "new_description", "checked": "new_description"},
        {
            "primary_modifiers": [
                Modifier.DEXTERITY.name.lower(),
            ],
            "checked": [Modifier.DEXTERITY.name.lower()],
        },
        {
            "hits": command_factory.class_hits_command_factory(starting_hits=8),
            "checked": model_factory.class_hits_model_factory(starting_hits=8),
        },
        {
            "proficiencies": command_factory.class_proficiencies_command_factory(
                weapons=[st_weapon.weapon_id]
            ),
            "checked": model_factory.class_proficiencies_model_factory(
                weapons=[st_weapon.weapon_id]
            ),
        },
        {
            "name_in_english": "new_name_in_english",
            "checked": "new_name_in_english",
        },
        {
            "source_id": st_source.source_id,
            "checked": st_source.source_id,
        },
    ],
    ids=[
        "name",
        "description",
        "primary_modifiers",
        "hits",
        "proficiencies",
        "name_in_english",
        "source_id",
    ],
)
async def test_update_ok(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
    update_field,
):
    await save_user(user_repository, st_user)
    await save_weapon(weapon_repository, st_weapon)
    await save_tool(tool_repository, st_tool)
    await save_source(source_repository, st_source)
    await save_class(class_repository, st_class)
    use_case = UpdateClassUseCase(
        class_service(class_repository),
        user_repository,
        class_repository,
        weapon_repository,
        tool_repository,
        source_repository,
    )
    checked = update_field.pop("checked")
    await use_case.execute(
        command_factory.ClassCommandFactory.update(
            user_id=st_user.user_id, class_id=st_class.class_id, **update_field
        )
    )
    updated_class = await class_repository.get_by_id(st_class.class_id)
    assert getattr(updated_class, list(update_field.keys())[0]) == checked


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,entity,error_status",
    [
        [
            {
                "proficiencies": command_factory.class_proficiencies_command_factory(
                    weapons=[st_weapon.weapon_id]
                ),
                "class_id": st_class.class_id,
            },
            "weapon",
            error.DomainErrorStatus.INVALID_DATA,
        ],
        [
            {
                "proficiencies": command_factory.class_proficiencies_command_factory(
                    tools=[st_tool.tool_id]
                ),
                "class_id": st_class.class_id,
            },
            "tool",
            error.DomainErrorStatus.INVALID_DATA,
        ],
        [
            {"source_id": st_source.source_id, "class_id": st_class.class_id},
            "source",
            error.DomainErrorStatus.INVALID_DATA,
        ],
        [
            {"class_id": st_class.class_id, "name": "new_name"},
            "class",
            error.DomainErrorStatus.NOT_FOUND,
        ],
    ],
    ids=["weapon", "tool", "source", "class"],
)
async def test_update_not_exists(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
    update_field,
    entity,
    error_status,
):
    await save_user(user_repository, st_user)
    if entity != "weapon":
        await save_weapon(weapon_repository, st_weapon)
    if entity != "tool":
        await save_tool(tool_repository, st_tool)
    if entity != "source":
        await save_source(source_repository, st_source)
    if entity != "class":
        await save_class(class_repository, st_class)
    use_case = UpdateClassUseCase(
        class_service(class_repository),
        user_repository,
        class_repository,
        weapon_repository,
        tool_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.ClassCommandFactory.update(
                user_id=st_user.user_id, **update_field
            )
        )
    except error.DomainError as e:
        assert e.status == error_status
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_name_exists(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon(weapon_repository, st_weapon)
    await save_tool(tool_repository, st_tool)
    await save_source(source_repository, st_source)
    await save_class(class_repository, st_class)
    renamed_class = model_factory.class_model_factory(
        name="second_name", class_id=uuid4()
    )
    await save_class(class_repository, renamed_class)
    use_case = UpdateClassUseCase(
        class_service(class_repository),
        user_repository,
        class_repository,
        weapon_repository,
        tool_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.ClassCommandFactory.update(
                user_id=st_user.user_id,
                class_id=renamed_class.class_id,
                name=st_class.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon(weapon_repository, st_weapon)
    await save_tool(tool_repository, st_tool)
    await save_source(source_repository, st_source)
    await save_class(class_repository, st_class)
    use_case = DeleteClassUseCase(user_repository, class_repository)
    await use_case.execute(
        command_factory.ClassCommandFactory.delete(
            user_id=st_user.user_id, class_id=st_class.class_id
        )
    )
    assert not await class_repository.id_exists(st_class.class_id)


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon(weapon_repository, st_weapon)
    await save_tool(tool_repository, st_tool)
    await save_source(source_repository, st_source)
    await save_class(class_repository, st_class)
    use_case = DeleteClassUseCase(user_repository, class_repository)
    try:
        await use_case.execute(
            command_factory.ClassCommandFactory.delete(
                user_id=st_user.user_id, class_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_class_ok(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon(weapon_repository, st_weapon)
    await save_tool(tool_repository, st_tool)
    await save_source(source_repository, st_source)
    await save_class(class_repository, st_class)
    use_case = GetClassUseCase(class_repository)
    result = await use_case.execute(
        query_factory.ClassQueryFactory.query(class_id=st_class.class_id)
    )
    assert result.class_id == st_class.class_id


@pytest.mark.asyncio
async def test_get_class_fail(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon(weapon_repository, st_weapon)
    await save_tool(tool_repository, st_tool)
    await save_source(source_repository, st_source)
    await save_class(class_repository, st_class)
    use_case = GetClassUseCase(class_repository)
    try:
        result = await use_case.execute(
            query_factory.ClassQueryFactory.query(class_id=uuid4())
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_classes_ok(
    user_repository,
    class_repository,
    weapon_repository,
    tool_repository,
    source_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon(weapon_repository, st_weapon)
    await save_tool(tool_repository, st_tool)
    await save_source(source_repository, st_source)
    await save_class(class_repository, st_class)
    use_case = GetClassesUseCase(class_repository)
    result = await use_case.execute(query_factory.ClassQueryFactory.queries())
    assert len(result) > 0
    result = await use_case.execute(
        query_factory.ClassQueryFactory.queries(search_by_name="random_symbols")
    )
    assert len(result) == 0
