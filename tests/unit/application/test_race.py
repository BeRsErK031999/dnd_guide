from itertools import count
from uuid import uuid4

import pytest
from application.use_case.command.race import (
    CreateRaceUseCase,
    DeleteRaceUseCase,
    UpdateRaceUseCase,
)
from application.use_case.query.race import GetRacesUseCase, GetRaceUseCase
from domain import error
from domain.creature_size import CreatureSize
from domain.creature_type import CreatureType
from domain.modifier import Modifier
from domain.race import RaceService
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_race = model_factory.race_model_factory()
st_source = model_factory.source_model_factory()


def race_service(race_repository):
    return RaceService(race_repository)


async def save_user(user_repository, user):
    await user_repository.create(user)


async def save_race(race_repository, race):
    await race_repository.create(race)


async def save_source(source_repository, source):
    await source_repository.create(source)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_field,checked",
    [
        [{"name": "random_name"}, {"name": "random_name"}],
        [{"description": "random_name"}, {"description": "random_name"}],
        [
            {"creature_type": CreatureType.ELEMENTAL.name.lower()},
            {"creature_type": CreatureType.ELEMENTAL.name.lower()},
        ],
        [
            {"creature_size": CreatureSize.TINY.name.lower()},
            {"creature_size": CreatureSize.TINY.name.lower()},
        ],
        [
            {
                "speed": command_factory.race_speed_command_factory(
                    base_speed=command_factory.length_command_factory(count=10),
                    description="description",
                )
            },
            {
                "speed": model_factory.race_speed_model_factory(
                    base_speed=model_factory.length_model_factory(count=10),
                    description="description",
                )
            },
        ],
        [
            {
                "age": command_factory.race_age_command_factory(
                    max_age=50, description="description"
                )
            },
            {
                "age": model_factory.race_age_model_factory(
                    max_age=50, description="description"
                )
            },
        ],
        [
            {
                "increase_modifiers": [
                    command_factory.race_increase_modifier_command_factory(
                        modifier=Modifier.DEXTERITY.name.lower(), bonus=3
                    )
                ]
            },
            {
                "increase_modifiers": [
                    model_factory.race_increase_modifier_model_factory(
                        modifier=Modifier.DEXTERITY.name.lower(), bonus=3
                    )
                ]
            },
        ],
        [
            {
                "features": [
                    command_factory.race_feature_command_factory(
                        name="name", description="description"
                    )
                ]
            },
            {
                "features": [
                    model_factory.race_feature_model_factory(
                        name="name", description="description"
                    )
                ]
            },
        ],
        [{"name_in_english": "random_name"}, {"name_in_english": "random_name"}],
    ],
    ids=[
        "name",
        "description",
        "creature_type",
        "creature_size",
        "speed",
        "age",
        "increase_modifiers",
        "features",
        "name_in_english",
    ],
)
async def test_create_ok(
    user_repository, race_repository, source_repository, create_field, checked
):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    use_case = CreateRaceUseCase(
        race_service(race_repository),
        user_repository,
        race_repository,
        source_repository,
    )
    result = await use_case.execute(
        command_factory.RaceCommandFactory.create(
            user_id=st_user.user_id, source_id=st_source.source_id, **create_field
        )
    )
    race = await race_repository.get_by_id(result)
    assert getattr(race, list(checked.keys())[0]) == list(checked.values())[0]


@pytest.mark.asyncio
async def test_create_name_exists(user_repository, race_repository, source_repository):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    await save_race(race_repository, st_race)
    use_case = CreateRaceUseCase(
        race_service(race_repository),
        user_repository,
        race_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.RaceCommandFactory.create(
                user_id=st_user.user_id,
                source_id=st_source.source_id,
                name=st_race.name,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_create_source_not_exists(
    user_repository, race_repository, source_repository
):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    use_case = CreateRaceUseCase(
        race_service(race_repository),
        user_repository,
        race_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.RaceCommandFactory.create(
                user_id=st_user.user_id, source_id=uuid4()
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
        [{"name": "random_name"}, {"name": "random_name"}],
        [{"description": "random_name"}, {"description": "random_name"}],
        [
            {"creature_type": CreatureType.ELEMENTAL.name.lower()},
            {"creature_type": CreatureType.ELEMENTAL.name.lower()},
        ],
        [
            {"creature_size": CreatureSize.TINY.name.lower()},
            {"creature_size": CreatureSize.TINY.name.lower()},
        ],
        [
            {
                "speed": command_factory.race_speed_command_factory(
                    base_speed=command_factory.length_command_factory(count=10),
                    description="description",
                )
            },
            {
                "speed": model_factory.race_speed_model_factory(
                    base_speed=model_factory.length_model_factory(count=10),
                    description="description",
                )
            },
        ],
        [
            {
                "age": command_factory.race_age_command_factory(
                    max_age=50, description="description"
                )
            },
            {
                "age": model_factory.race_age_model_factory(
                    max_age=50, description="description"
                )
            },
        ],
        [
            {
                "increase_modifiers": [
                    command_factory.race_increase_modifier_command_factory(
                        modifier=Modifier.DEXTERITY.name.lower(), bonus=3
                    )
                ]
            },
            {
                "increase_modifiers": [
                    model_factory.race_increase_modifier_model_factory(
                        modifier=Modifier.DEXTERITY.name.lower(), bonus=3
                    )
                ]
            },
        ],
        [
            {
                "new_features": [
                    command_factory.race_feature_command_factory(
                        name="name", description="description"
                    )
                ]
            },
            {
                "features": [
                    model_factory.race_feature_model_factory(
                        name="name", description="description"
                    )
                ]
            },
        ],
        [
            {
                "add_features": [
                    command_factory.race_feature_command_factory(
                        name="name", description="description"
                    )
                ]
            },
            {
                "features": [
                    *st_race.features,
                    model_factory.race_feature_model_factory(
                        name="name", description="description"
                    ),
                ]
            },
        ],
        [
            {"remove_features": [f.name for f in st_race.features]},
            {"features": []},
        ],
        [{"name_in_english": "random_name"}, {"name_in_english": "random_name"}],
        [{"source_id": st_source.source_id}, {"source_id": st_source.source_id}],
    ],
    ids=[
        "name",
        "description",
        "creature_type",
        "creature_size",
        "speed",
        "age",
        "increase_modifiers",
        "new_features",
        "add_features",
        "remove_features",
        "name_in_english",
        "source",
    ],
)
async def test_update_ok(
    user_repository, race_repository, source_repository, update_field, checked
):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    await save_race(race_repository, st_race)
    use_case = UpdateRaceUseCase(
        race_service(race_repository),
        user_repository,
        race_repository,
        source_repository,
    )
    await use_case.execute(
        command_factory.RaceCommandFactory.update(
            user_id=st_user.user_id, race_id=st_race.race_id, **update_field
        )
    )
    updated_race = await race_repository.get_by_id(st_race.race_id)
    assert getattr(updated_race, list(checked.keys())[0]) == list(checked.values())[0]


@pytest.mark.asyncio
async def test_update_source_not_exists(
    user_repository, race_repository, source_repository
):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    await save_race(race_repository, st_race)
    use_case = UpdateRaceUseCase(
        race_service(race_repository),
        user_repository,
        race_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.RaceCommandFactory.update(
                user_id=st_user.user_id, race_id=st_race.race_id, source_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_race_not_exists(
    user_repository, race_repository, source_repository
):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    use_case = UpdateRaceUseCase(
        race_service(race_repository),
        user_repository,
        race_repository,
        source_repository,
    )
    try:
        await use_case.execute(
            command_factory.RaceCommandFactory.update(
                user_id=st_user.user_id, race_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(user_repository, race_repository, source_repository):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    await save_race(race_repository, st_race)
    use_case = DeleteRaceUseCase(
        user_repository,
        race_repository,
    )
    await use_case.execute(
        command_factory.RaceCommandFactory.delete(
            user_id=st_user.user_id, race_id=st_race.race_id
        )
    )
    assert not await race_repository.id_exists(st_race.race_id)


@pytest.mark.asyncio
async def test_delete_race_not_exists(
    user_repository, race_repository, source_repository
):
    await save_user(user_repository, st_user)
    await save_source(source_repository, st_source)
    use_case = DeleteRaceUseCase(
        user_repository,
        race_repository,
    )
    try:
        await use_case.execute(
            command_factory.RaceCommandFactory.delete(
                user_id=st_user.user_id, race_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_race_ok(race_repository):
    await save_race(race_repository, st_race)
    use_case = GetRaceUseCase(race_repository)
    result = await use_case.execute(
        query_factory.RaceQueryFactory.query(race_id=st_race.race_id)
    )
    assert result == st_race


@pytest.mark.asyncio
async def test_get_race_not_exists(race_repository):
    await save_race(race_repository, st_race)
    use_case = GetRaceUseCase(race_repository)
    try:
        await use_case.execute(query_factory.RaceQueryFactory.query(race_id=uuid4()))
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"search_by_name": st_race.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [dict(), 1],
    ],
    ids=["one", "zero", "all"],
)
async def test_get_races_ok(race_repository, filters, count):
    await save_race(race_repository, st_race)
    use_case = GetRacesUseCase(race_repository)
    result = await use_case.execute(query_factory.RaceQueryFactory.queries(**filters))
    assert len(result) == count
