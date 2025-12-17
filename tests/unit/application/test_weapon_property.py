import pytest
from application.use_case.command.weapon_property import (
    CreateWeaponPropertyUseCase,
    DeleteWeaponPropertyUseCase,
    UpdateWeaponPropertyUseCase,
)
from application.use_case.query.weapon_property import (
    GetWeaponPropertiesUseCase,
    GetWeaponPropertyUseCase,
)
from domain import error
from domain.dice import DiceType
from domain.weapon_property import WeaponPropertyService
from domain.weapon_property.name import WeaponPropertyName
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_property = model_factory.weapon_property_model_factory()


def property_service(property_repository):
    return WeaponPropertyService(property_repository)


async def save_user(user_repository, user):
    await user_repository.save(user)


async def save_property(property_repository, weapon_property):
    await property_repository.save(weapon_property)


async def save_weapon(weapon_repository, weapon):
    await weapon_repository.save(weapon)


@pytest.mark.asyncio
async def test_create_ok(user_repository, weapon_property_repository):
    await save_user(user_repository, st_user)
    use_case = CreateWeaponPropertyUseCase(
        property_service(weapon_property_repository),
        user_repository,
        weapon_property_repository,
    )
    result = await use_case.execute(
        command_factory.WeaponPropertyCommandFactory.create(
            user_id=st_user.user_id,
        )
    )
    assert await weapon_property_repository.id_exists(result)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field,checked_field,checked_value",
    [
        [
            {"name": WeaponPropertyName.FINESSE.name.lower()},
            "name",
            WeaponPropertyName.FINESSE.name.lower(),
        ],
        [{"description": "new_name"}, "description", "new_name"],
        [
            {
                "base_range": command_factory.weapon_property_base_range_command_factory(
                    range=command_factory.length_command_factory(count=10)
                ),
                "max_range": command_factory.weapon_property_max_range_command_factory(
                    range=command_factory.length_command_factory(count=10)
                ),
                "name": WeaponPropertyName.AMMUNITION.name.lower(),
            },
            "base_range",
            model_factory.length_model_factory(count=10),
        ],
        [
            {
                "base_range": command_factory.weapon_property_base_range_command_factory(
                    range=command_factory.length_command_factory(count=10)
                ),
                "max_range": command_factory.weapon_property_max_range_command_factory(
                    range=command_factory.length_command_factory(count=10)
                ),
                "name": WeaponPropertyName.AMMUNITION.name.lower(),
            },
            "max_range",
            model_factory.length_model_factory(count=10),
        ],
        [
            {
                "second_hand_dice": command_factory.weapon_property_second_hand_dice_command_factory(
                    dice=command_factory.dice_command_factory(
                        count=1, dice_type=DiceType.D6.name.lower()
                    )
                ),
                "name": WeaponPropertyName.VERSATILE.name.lower(),
            },
            "second_hand_dice",
            model_factory.dice_model_factory(
                count=1, dice_type=DiceType.D6.name.lower()
            ),
        ],
    ],
    ids=[
        "name",
        "description",
        "base_range",
        "max_range",
        "second_hand_dice",
    ],
)
async def test_update_ok(
    user_repository,
    weapon_property_repository,
    update_field,
    checked_field,
    checked_value,
):
    await save_user(user_repository, st_user)
    await save_property(weapon_property_repository, st_property)
    use_case = UpdateWeaponPropertyUseCase(
        property_service(weapon_property_repository),
        user_repository,
        weapon_property_repository,
    )
    await use_case.execute(
        command_factory.WeaponPropertyCommandFactory.update(
            user_id=st_user.user_id,
            property_id=st_property.weapon_property_id,
            **update_field,
        )
    )
    updated_property = await weapon_property_repository.get_by_id(
        st_property.weapon_property_id
    )
    assert getattr(updated_property, checked_field) == checked_value


@pytest.mark.asyncio
async def test_update_not_exists(user_repository, weapon_property_repository):
    await save_user(user_repository, st_user)
    use_case = UpdateWeaponPropertyUseCase(
        property_service(weapon_property_repository),
        user_repository,
        weapon_property_repository,
    )
    try:
        await use_case.execute(
            command_factory.WeaponPropertyCommandFactory.update(
                user_id=st_user.user_id,
                property_id=st_property.weapon_property_id,
                name=WeaponPropertyName.FINESSE.name.lower(),
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(
    user_repository, weapon_property_repository, weapon_repository
):
    await save_user(user_repository, st_user)
    await save_property(weapon_property_repository, st_property)
    use_case = DeleteWeaponPropertyUseCase(
        user_repository, weapon_property_repository, weapon_repository
    )
    await use_case.execute(
        command_factory.WeaponPropertyCommandFactory.delete(
            user_id=st_user.user_id, property_id=st_property.weapon_property_id
        )
    )
    assert not await weapon_property_repository.id_exists(
        st_property.weapon_property_id
    )


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository, weapon_property_repository, weapon_repository
):
    await save_user(user_repository, st_user)
    use_case = DeleteWeaponPropertyUseCase(
        user_repository, weapon_property_repository, weapon_repository
    )
    try:
        await use_case.execute(
            command_factory.WeaponPropertyCommandFactory.delete(
                user_id=st_user.user_id, property_id=st_property.weapon_property_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_with_weapon(
    user_repository, weapon_property_repository, weapon_repository
):
    await save_user(user_repository, st_user)
    await save_property(weapon_property_repository, st_property)
    weapon = model_factory.weapon_model_factory(
        weapon_property_ids=[st_property.weapon_property_id]
    )
    await save_weapon(weapon_repository, weapon)
    use_case = DeleteWeaponPropertyUseCase(
        user_repository, weapon_property_repository, weapon_repository
    )
    try:
        await use_case.execute(
            command_factory.WeaponPropertyCommandFactory.delete(
                user_id=st_user.user_id, property_id=st_property.weapon_property_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_property_ok(weapon_property_repository):
    await save_property(weapon_property_repository, st_property)
    use_case = GetWeaponPropertyUseCase(weapon_property_repository)
    result = await use_case.execute(
        query_factory.WeaponPropertyQueryFactory.query(
            property_id=st_property.weapon_property_id
        )
    )
    assert result == st_property


@pytest.mark.asyncio
async def test_get_property_not_exists(weapon_property_repository):
    use_case = GetWeaponPropertyUseCase(weapon_property_repository)
    try:
        await use_case.execute(
            query_factory.WeaponPropertyQueryFactory.query(
                property_id=st_property.weapon_property_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [{"search_by_name": st_property.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [dict(), 1],
    ],
)
async def test_get_properties_ok(weapon_property_repository, filters, count):
    await save_property(weapon_property_repository, st_property)
    use_case = GetWeaponPropertiesUseCase(weapon_property_repository)
    result = await use_case.execute(
        query_factory.WeaponPropertyQueryFactory.queries(**filters)
    )
    assert len(result) == count
