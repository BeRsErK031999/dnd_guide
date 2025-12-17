from uuid import uuid4

import pytest
from application.use_case.command.source import (
    CreateSourceUseCase,
    DeleteSourceUseCase,
    UpdateSourceUseCase,
)
from application.use_case.query.source import GetSourcesUseCase, GetSourceUseCase
from domain import error
from domain.source import SourceService
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_source = model_factory.source_model_factory()


def source_service(source_repository):
    return SourceService(source_repository)


async def save_user(user_repository, user):
    await user_repository.save(user)


async def save_source(source_repository, source):
    await source_repository.save(source)


async def save_spell(spell_repository, spell):
    await spell_repository.save(spell)


async def save_class(class_repository, character_class):
    await class_repository.save(character_class)


async def save_race(race_repository, race):
    await race_repository.save(race)


@pytest.mark.asyncio
async def test_create_ok(user_repository, source_repository):
    await save_user(user_repository, st_user)
    use_case = CreateSourceUseCase(
        source_service(source_repository), user_repository, source_repository
    )
    result = await use_case.execute(
        command_factory.SourceCommandFactory.create(user_id=st_user.user_id)
    )
    assert await source_repository.id_exists(result)


@pytest.mark.asyncio
async def test_create_name_exists(user_repository, source_repository):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    use_case = CreateSourceUseCase(
        source_service(source_repository), user_repository, source_repository
    )
    try:
        await use_case.execute(
            command_factory.SourceCommandFactory.create(
                user_id=st_user.user_id, name=st_source.name
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
        [{"name_in_english": "new_name"}, "name_in_english", "new_name"],
    ],
    ids=["name", "description", "name_in_english"],
)
async def test_update_ok(
    user_repository, source_repository, update_field, checked_field, checked_value
):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    use_case = UpdateSourceUseCase(
        source_service(source_repository), user_repository, source_repository
    )
    await use_case.execute(
        command_factory.SourceCommandFactory.update(
            user_id=st_user.user_id, source_id=st_source.source_id, **update_field
        )
    )
    updated_source = await source_repository.get_by_id(st_source.source_id)
    assert getattr(updated_source, checked_field) == checked_value


@pytest.mark.asyncio
async def test_update_name_exists(user_repository, source_repository):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    exists_source = model_factory.source_model_factory(
        source_id=uuid4(), name="second_name"
    )
    await save_source(source_repository, exists_source)
    use_case = UpdateSourceUseCase(
        source_service(source_repository), user_repository, source_repository
    )
    try:
        await use_case.execute(
            command_factory.SourceCommandFactory.update(
                user_id=st_user.user_id,
                source_id=st_source.source_id,
                name=exists_source.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_not_exists(user_repository, source_repository):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    use_case = UpdateSourceUseCase(
        source_service(source_repository), user_repository, source_repository
    )
    try:
        await use_case.execute(
            command_factory.SourceCommandFactory.update(
                user_id=st_user.user_id, source_id=uuid4(), name="new_name"
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(
    user_repository,
    source_repository,
    spell_repository,
    class_repository,
    race_repository,
):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    use_case = DeleteSourceUseCase(
        user_repository,
        source_repository,
        spell_repository,
        class_repository,
        race_repository,
    )
    await use_case.execute(
        command_factory.SourceCommandFactory.delete(
            user_id=st_user.user_id, source_id=st_source.source_id
        )
    )
    assert not await source_repository.id_exists(st_source.source_id)


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository,
    source_repository,
    spell_repository,
    class_repository,
    race_repository,
):
    await save_user(user_repository, st_user)
    use_case = DeleteSourceUseCase(
        user_repository,
        source_repository,
        spell_repository,
        class_repository,
        race_repository,
    )
    try:
        await use_case.execute(
            command_factory.SourceCommandFactory.delete(
                user_id=st_user.user_id, source_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exists", ["spell", "class", "race"], ids=["spell", "class", "race"]
)
async def test_delete_with_spell(
    user_repository,
    source_repository,
    spell_repository,
    class_repository,
    race_repository,
    exists,
):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    if exists == "spell":
        await save_spell(
            spell_repository,
            model_factory.spell_model_factory(source_id=st_source.source_id),
        )
    if exists == "class":
        await save_class(
            class_repository,
            model_factory.class_model_factory(source_id=st_source.source_id),
        )
    if exists == "race":
        await save_race(
            race_repository,
            model_factory.race_model_factory(source_id=st_source.source_id),
        )
    use_case = DeleteSourceUseCase(
        user_repository,
        source_repository,
        class_repository,
        race_repository,
        spell_repository,
    )
    try:
        await use_case.execute(
            command_factory.SourceCommandFactory.delete(
                user_id=st_user.user_id, source_id=st_source.source_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_source_ok(source_repository):
    await save_source(source_repository, st_source)
    use_case = GetSourceUseCase(source_repository)
    result = await use_case.execute(
        query_factory.SourceQueryFactory.query(source_id=st_source.source_id)
    )
    assert result == st_source


@pytest.mark.asyncio
async def test_get_source_not_exists(source_repository):
    await save_source(source_repository, st_source)
    use_case = GetSourceUseCase(source_repository)
    try:
        await use_case.execute(
            query_factory.SourceQueryFactory.query(source_id=uuid4())
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"search_by_name": st_source.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [dict(), 1],
    ],
    ids=["one", "zero", "all"],
)
async def test_get_sources_ok(source_repository, filters, count):
    await save_source(source_repository, st_source)
    use_case = GetSourcesUseCase(source_repository)
    result = await use_case.execute(query_factory.SourceQueryFactory.queries(**filters))
    assert len(result) == count
