from uuid import uuid4

import pytest
from application.use_case.command.class_level import (
    CreateClassLevelUseCase,
    DeleteClassLevelUseCase,
    UpdateClassLevelUseCase,
)
from application.use_case.query.class_level import (
    GetClassLevelsUseCase,
    GetClassLevelUseCase,
)
from domain import error
from domain.class_level import ClassLevelService
from domain.dice import DiceType
from tests.factories import command_factory, model_factory, query_factory

st_class = model_factory.class_model_factory()
st_user = model_factory.user_model_factory()
st_level = model_factory.class_level_model_factory()


def class_level_service(class_level_repository):
    return ClassLevelService(class_level_repository)


async def save_user(user_repository, user):
    await user_repository.create(user)


async def save_class(class_repository, character_class):
    await class_repository.create(character_class)


async def save_class_level(class_level_repository, class_level):
    await class_level_repository.create(class_level)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_field,checked",
    [
        [{"level": 2}, {"level": 2}],
        [
            {
                "dice": command_factory.class_level_dice_command_factory(
                    hit_dice=command_factory.dice_command_factory(
                        count=2, dice_type=DiceType.D10.name.lower()
                    ),
                    description="description",
                )
            },
            {
                "dice": model_factory.class_level_dice_model_factory(
                    hit_dice=model_factory.dice_model_factory(
                        count=2, dice_type=DiceType.D10.name.lower()
                    ),
                    description="description",
                )
            },
        ],
        [
            {"spell_slots": [1, 1, 1, 1, 1, 1, 1, 1, 1]},
            {"spell_slots": [1, 1, 1, 1, 1, 1, 1, 1, 1]},
        ],
        [{"number_cantrips_know": 2}, {"number_cantrips_know": 2}],
        [{"number_spells_know": 2}, {"number_spells_know": 2}],
        [{"number_arcanums_know": 2}, {"number_arcanums_know": 2}],
        [
            {
                "points": command_factory.class_level_points_command_factory(
                    points=3, description="description"
                )
            },
            {
                "points": model_factory.class_level_points_model_factory(
                    points=3, description="description"
                )
            },
        ],
        [
            {
                "bonus_damage": command_factory.class_level_bonus_damage_command_factory(
                    damage=3, description="description"
                )
            },
            {
                "bonus_damage": model_factory.class_level_bonus_damage_model_factory(
                    damage=3, description="description"
                )
            },
        ],
        [
            {
                "increase_speed": command_factory.class_level_increase_speed_command_factory(
                    speed=command_factory.length_command_factory(count=10),
                    description="description",
                )
            },
            {
                "increase_speed": model_factory.class_level_increase_speed_model_factory(
                    speed=model_factory.length_model_factory(count=10),
                    description="description",
                )
            },
        ],
    ],
    ids=[
        "level",
        "dice",
        "spell_slots",
        "number_cantrips_know",
        "number_spells_know",
        "number_arcanums_know",
        "points",
        "bonus_damage",
        "increase_speed",
    ],
)
async def test_create_ok(
    user_repository, class_repository, class_level_repository, create_field, checked
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    use_case = CreateClassLevelUseCase(
        class_level_service(class_level_repository),
        user_repository,
        class_level_repository,
        class_repository,
    )
    result = await use_case.execute(
        command_factory.ClassLevelCommandFactory.create(
            user_id=st_user.user_id, class_id=st_class.class_id, **create_field
        )
    )
    level = await class_level_repository.get_by_id(result)
    assert getattr(level, list(checked.keys())[0]) == list(checked.values())[0]


@pytest.mark.asyncio
async def test_create_class_not_exists(
    user_repository, class_repository, class_level_repository
):
    await save_user(user_repository, st_user)
    use_case = CreateClassLevelUseCase(
        class_level_service(class_level_repository),
        user_repository,
        class_level_repository,
        class_repository,
    )
    try:
        await use_case.execute(
            command_factory.ClassLevelCommandFactory.create(
                user_id=st_user.user_id, class_id=st_class.class_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_create_level_exists(
    user_repository, class_repository, class_level_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    exists_level = model_factory.class_level_model_factory(
        class_id=st_class.class_id, level=1
    )
    await save_class_level(class_level_repository, exists_level)
    use_case = CreateClassLevelUseCase(
        class_level_service(class_level_repository),
        user_repository,
        class_level_repository,
        class_repository,
    )
    try:
        await use_case.execute(
            command_factory.ClassLevelCommandFactory.create(
                user_id=st_user.user_id, class_id=st_class.class_id
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
        [{"class_id": st_class.class_id}, {"class_id": st_class.class_id}],
        [{"level": 3}, {"level": 3}],
        [
            {
                "dice": command_factory.class_level_dice_command_factory(
                    hit_dice=command_factory.dice_command_factory(
                        count=3, dice_type=DiceType.D10.name.lower()
                    ),
                    description="description",
                )
            },
            {
                "dice": model_factory.class_level_dice_model_factory(
                    hit_dice=model_factory.dice_model_factory(
                        count=3, dice_type=DiceType.D10.name.lower()
                    ),
                    description="description",
                )
            },
        ],
        [{"spell_slots": [2, 2, 2, 2, 2]}, {"spell_slots": [2, 2, 2, 2, 2]}],
        [{"number_cantrips_know": 3}, {"number_cantrips_know": 3}],
        [{"number_spells_know": 3}, {"number_spells_know": 3}],
        [{"number_arcanums_know": 3}, {"number_arcanums_know": 3}],
        [
            {
                "points": command_factory.class_level_points_command_factory(
                    points=3, description="description"
                )
            },
            {
                "points": model_factory.class_level_points_model_factory(
                    points=3, description="description"
                )
            },
        ],
        [
            {
                "bonus_damage": command_factory.class_level_bonus_damage_command_factory(
                    damage=3, description="description"
                )
            },
            {
                "bonus_damage": model_factory.class_level_bonus_damage_model_factory(
                    damage=3, description="description"
                )
            },
        ],
        [
            {
                "increase_speed": command_factory.class_level_increase_speed_command_factory(
                    speed=command_factory.length_command_factory(count=3),
                    description="description",
                )
            },
            {
                "increase_speed": model_factory.class_level_increase_speed_model_factory(
                    speed=model_factory.length_model_factory(count=3),
                    description="description",
                )
            },
        ],
    ],
    ids=[
        "class_id",
        "level",
        "dice",
        "spell_slots",
        "number_cantrips_know",
        "number_spells_know",
        "number_arcanums_know",
        "points",
        "bonus_damage",
        "increase_speed",
    ],
)
async def test_update_ok(
    user_repository, class_repository, class_level_repository, update_field, checked
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_class_level(class_level_repository, st_level)
    use_case = UpdateClassLevelUseCase(
        class_level_service(class_level_repository),
        user_repository,
        class_level_repository,
        class_repository,
    )
    await use_case.execute(
        command_factory.ClassLevelCommandFactory.update(
            user_id=st_user.user_id,
            class_level_id=st_level.class_level_id,
            **update_field,
        )
    )
    level = await class_level_repository.get_by_id(st_level.class_level_id)
    assert getattr(level, list(checked.keys())[0]) == list(checked.values())[0]


@pytest.mark.asyncio
async def test_update_class_not_exists(
    user_repository, class_repository, class_level_repository
):
    await save_user(user_repository, st_user)
    await save_class_level(class_level_repository, st_level)
    use_case = UpdateClassLevelUseCase(
        class_level_service(class_level_repository),
        user_repository,
        class_level_repository,
        class_repository,
    )
    try:
        await use_case.execute(
            command_factory.ClassLevelCommandFactory.update(
                user_id=st_user.user_id, class_level_id=st_level.class_level_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_level_exists(
    user_repository, class_repository, class_level_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    exists_level = model_factory.class_level_model_factory(
        class_id=st_class.class_id, level=1
    )
    await save_class_level(class_level_repository, exists_level)
    use_case = UpdateClassLevelUseCase(
        class_level_service(class_level_repository),
        user_repository,
        class_level_repository,
        class_repository,
    )
    try:
        await use_case.execute(
            command_factory.ClassLevelCommandFactory.update(
                user_id=st_user.user_id,
                class_level_id=st_level.class_level_id,
                class_id=st_class.class_id,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(user_repository, class_repository, class_level_repository):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_class_level(class_level_repository, st_level)
    use_case = DeleteClassLevelUseCase(
        user_repository,
        class_level_repository,
    )
    await use_case.execute(
        command_factory.ClassLevelCommandFactory.delete(
            user_id=st_user.user_id, class_level_id=st_level.class_level_id
        )
    )
    assert not await class_level_repository.id_exists(st_level.class_level_id)


@pytest.mark.asyncio
async def test_get_level_ok(user_repository, class_repository, class_level_repository):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_class_level(class_level_repository, st_level)
    use_case = GetClassLevelUseCase(class_level_repository)
    result = await use_case.execute(
        query_factory.ClassLevelQueryFactory.query(level_id=st_level.class_level_id)
    )
    assert result == st_level


@pytest.mark.asyncio
async def test_get_level_not_exists(
    user_repository, class_repository, class_level_repository
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    use_case = GetClassLevelUseCase(class_level_repository)
    try:
        await use_case.execute(
            query_factory.ClassLevelQueryFactory.query(level_id=st_level.class_level_id)
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter,count",
    [
        [{}, 1],
        [{"filter_by_class_id": st_level.class_id}, 1],
        [{"filter_by_class_id": uuid4()}, 0],
    ],
    ids=["all", "one", "zero"],
)
async def test_get_levels_ok(
    user_repository, class_repository, class_level_repository, filter, count
):
    await save_user(user_repository, st_user)
    await save_class(class_repository, st_class)
    await save_class_level(class_level_repository, st_level)
    use_case = GetClassLevelsUseCase(class_level_repository)
    result = await use_case.execute(
        query_factory.ClassLevelQueryFactory.queries(**filter)
    )
    assert len(result) == count
