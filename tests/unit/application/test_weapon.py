from uuid import uuid4

import pytest
from application.use_case.command.weapon import (
    CreateWeaponUseCase,
    DeleteWeaponUseCase,
    UpdateWeaponUseCase,
)
from application.use_case.query.weapon import GetWeaponsUseCase, GetWeaponUseCase
from domain import error
from domain.damage_type import DamageType
from domain.dice import DiceType
from domain.weapon import WeaponService
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_weapon = model_factory.weapon_model_factory()
st_kind = model_factory.weapon_kind_model_factory()
st_property = model_factory.weapon_property_model_factory()
st_material = model_factory.material_model_factory()


def weapon_service(weapon_repository):
    return WeaponService(weapon_repository)


async def save_user(user_repository, user):
    await user_repository.create(user)


async def save_weapon(weapon_repository, weapon):
    await weapon_repository.create(weapon)


async def save_weapon_kind(weapon_kind_repository, weapon_kind):
    await weapon_kind_repository.create(weapon_kind)


async def save_weapon_property(weapon_property_repository, weapon_property):
    await weapon_property_repository.create(weapon_property)


async def save_material(material_repository, material):
    await material_repository.create(material)


@pytest.mark.asyncio
async def test_create_ok(
    user_repository,
    weapon_repository,
    weapon_kind_repository,
    weapon_property_repository,
    material_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon_kind(weapon_kind_repository, st_kind)
    await save_weapon_property(weapon_property_repository, st_property)
    await save_material(material_repository, st_material)
    use_case = CreateWeaponUseCase(
        weapon_service(weapon_repository),
        user_repository,
        weapon_repository,
        weapon_kind_repository,
        weapon_property_repository,
        material_repository,
    )
    result = await use_case.execute(
        command_factory.WeaponCommandFactory.create(
            user_id=st_user.user_id,
            weapon_kind_id=st_kind.weapon_kind_id,
            weapon_property_ids=[st_property.weapon_property_id],
            material_id=st_material.material_id,
        )
    )
    created_weapon = await weapon_repository.get_by_id(result)
    assert created_weapon.weapon_kind_id == st_kind.weapon_kind_id
    assert created_weapon.weapon_property_ids == [st_property.weapon_property_id]
    assert created_weapon.material_id == st_material.material_id


@pytest.mark.asyncio
async def test_create_name_exists(
    user_repository,
    weapon_repository,
    weapon_kind_repository,
    weapon_property_repository,
    material_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon_kind(weapon_kind_repository, st_kind)
    await save_weapon_property(weapon_property_repository, st_property)
    await save_material(material_repository, st_material)
    await save_weapon(weapon_repository, st_weapon)
    use_case = CreateWeaponUseCase(
        weapon_service(weapon_repository),
        user_repository,
        weapon_repository,
        weapon_kind_repository,
        weapon_property_repository,
        material_repository,
    )
    try:
        await use_case.execute(
            command_factory.WeaponCommandFactory.create(
                user_id=st_user.user_id,
                name=st_weapon.name,
                weapon_kind_id=st_kind.weapon_kind_id,
                weapon_property_ids=[st_property.weapon_property_id],
                material_id=st_material.material_id,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "not_exists", ["kind", "property", "material"], ids=["kind", "property", "material"]
)
async def test_create_not_exists(
    user_repository,
    weapon_repository,
    weapon_kind_repository,
    weapon_property_repository,
    material_repository,
    not_exists,
):
    await save_user(user_repository, st_user)
    if not_exists == "kind":
        await save_weapon_kind(weapon_kind_repository, st_kind)
    if not_exists == "property":
        await save_weapon_property(weapon_property_repository, st_property)
    if not_exists == "material":
        await save_material(material_repository, st_material)
    use_case = CreateWeaponUseCase(
        weapon_service(weapon_repository),
        user_repository,
        weapon_repository,
        weapon_kind_repository,
        weapon_property_repository,
        material_repository,
    )
    try:
        await use_case.execute(
            command_factory.WeaponCommandFactory.create(
                user_id=st_user.user_id,
                name=st_weapon.name,
                weapon_kind_id=st_kind.weapon_kind_id,
                weapon_property_ids=[st_property.weapon_property_id],
                material_id=st_material.material_id,
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
        [
            {"weapon_kind_id": st_kind.weapon_kind_id},
            "weapon_kind_id",
            st_kind.weapon_kind_id,
        ],
        [{"name": "new_name"}, "name", "new_name"],
        [{"description": "new_name"}, "description", "new_name"],
        [
            {"cost": command_factory.coin_command_factory(count=100)},
            "cost",
            model_factory.coins_model_factory(count=100),
        ],
        [
            {
                "damage": command_factory.weapon_damage_command_factory(
                    dice=command_factory.dice_command_factory(
                        count=3, dice_type=DiceType.D12.name.lower()
                    ),
                    damage_type=DamageType.COLD.name.lower(),
                    bonus_damage=4,
                )
            },
            "damage",
            model_factory.weapon_damage_model_factory(
                dice=model_factory.dice_model_factory(
                    count=3, dice_type=DiceType.D12.name.lower()
                ),
                damage_type=DamageType.COLD.name.lower(),
                bonus_damage=4,
            ),
        ],
        [
            {"weight": command_factory.weight_command_factory(count=40)},
            "weight",
            model_factory.weight_model_factory(count=40),
        ],
        [
            {"weapon_property_ids": [st_property.weapon_property_id]},
            "weapon_property_ids",
            [st_property.weapon_property_id],
        ],
        [
            {"material_id": st_material.material_id},
            "material_id",
            st_material.material_id,
        ],
    ],
    ids=[
        "weapon_kind_id",
        "name",
        "description",
        "cost",
        "damage",
        "weight",
        "weapon_property_ids",
        "material_id",
    ],
)
async def test_update_ok(
    user_repository,
    weapon_repository,
    weapon_kind_repository,
    weapon_property_repository,
    material_repository,
    update_field,
    checked_field,
    checked_value,
):
    await save_user(user_repository, st_user)
    await save_weapon_kind(weapon_kind_repository, st_kind)
    await save_weapon_property(weapon_property_repository, st_property)
    await save_material(material_repository, st_material)
    await save_weapon(weapon_repository, st_weapon)
    use_case = UpdateWeaponUseCase(
        weapon_service(weapon_repository),
        user_repository,
        weapon_repository,
        weapon_kind_repository,
        weapon_property_repository,
        material_repository,
    )
    await use_case.execute(
        command_factory.WeaponCommandFactory.update(
            user_id=st_user.user_id, weapon_id=st_weapon.weapon_id, **update_field
        )
    )
    updated_weapon = await weapon_repository.get_by_id(st_weapon.weapon_id)
    assert getattr(updated_weapon, checked_field) == checked_value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "not_exists", ["kind", "property", "material"], ids=["kind", "property", "material"]
)
async def test_update_field_not_exists(
    user_repository,
    weapon_repository,
    weapon_kind_repository,
    weapon_property_repository,
    material_repository,
    not_exists,
):
    await save_user(user_repository, st_user)
    if not_exists == "kind":
        await save_weapon_kind(weapon_kind_repository, st_kind)
    if not_exists == "property":
        await save_weapon_property(weapon_property_repository, st_property)
    if not_exists == "material":
        await save_material(material_repository, st_material)
    await save_weapon(weapon_repository, st_weapon)
    use_case = UpdateWeaponUseCase(
        weapon_service(weapon_repository),
        user_repository,
        weapon_repository,
        weapon_kind_repository,
        weapon_property_repository,
        material_repository,
    )
    try:
        await use_case.execute(
            command_factory.WeaponCommandFactory.update(
                user_id=st_user.user_id,
                weapon_id=st_weapon.weapon_id,
                weapon_kind_id=st_kind.weapon_kind_id,
                weapon_property_ids=[st_property.weapon_property_id],
                material_id=st_material.material_id,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_not_exists(
    user_repository,
    weapon_repository,
    weapon_kind_repository,
    weapon_property_repository,
    material_repository,
):
    await save_user(user_repository, st_user)
    use_case = UpdateWeaponUseCase(
        weapon_service(weapon_repository),
        user_repository,
        weapon_repository,
        weapon_kind_repository,
        weapon_property_repository,
        material_repository,
    )
    try:
        await use_case.execute(
            command_factory.WeaponCommandFactory.update(
                user_id=st_user.user_id, weapon_id=st_weapon.weapon_id, name="new_name"
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(
    user_repository,
    weapon_repository,
    weapon_kind_repository,
    weapon_property_repository,
    material_repository,
    class_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon_kind(weapon_kind_repository, st_kind)
    await save_weapon_property(weapon_property_repository, st_property)
    await save_material(material_repository, st_material)
    await save_weapon(weapon_repository, st_weapon)
    use_case = DeleteWeaponUseCase(user_repository, weapon_repository, class_repository)
    await use_case.execute(
        command_factory.WeaponCommandFactory.delete(
            user_id=st_user.user_id, weapon_id=st_weapon.weapon_id
        )
    )
    assert not await weapon_repository.id_exists(st_weapon.weapon_id)


@pytest.mark.asyncio
async def test_delete_not_exists(
    user_repository,
    weapon_repository,
    weapon_kind_repository,
    weapon_property_repository,
    material_repository,
    class_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon_kind(weapon_kind_repository, st_kind)
    await save_weapon_property(weapon_property_repository, st_property)
    await save_material(material_repository, st_material)
    use_case = DeleteWeaponUseCase(user_repository, weapon_repository, class_repository)
    try:
        await use_case.execute(
            command_factory.WeaponCommandFactory.delete(
                user_id=st_user.user_id, weapon_id=st_weapon.weapon_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_with_class(
    user_repository,
    weapon_repository,
    weapon_kind_repository,
    weapon_property_repository,
    material_repository,
    class_repository,
):
    await save_user(user_repository, st_user)
    await save_weapon_kind(weapon_kind_repository, st_kind)
    await save_weapon_property(weapon_property_repository, st_property)
    await save_material(material_repository, st_material)
    await save_weapon(weapon_repository, st_weapon)
    exists_class = model_factory.class_model_factory(
        proficiencies=model_factory.class_proficiencies_model_factory(
            weapons=[st_weapon.weapon_id]
        )
    )
    await class_repository.create(exists_class)
    use_case = DeleteWeaponUseCase(user_repository, weapon_repository, class_repository)
    try:
        await use_case.execute(
            command_factory.WeaponCommandFactory.delete(
                user_id=st_user.user_id, weapon_id=st_weapon.weapon_id
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_weapon_ok(weapon_repository):
    await save_weapon(weapon_repository, st_weapon)
    use_case = GetWeaponUseCase(weapon_repository)
    result = await use_case.execute(
        query_factory.WeaponQueryFactory.query(st_weapon.weapon_id)
    )
    assert result == st_weapon


@pytest.mark.asyncio
async def test_get_weapon_not_exists(weapon_repository):
    use_case = GetWeaponUseCase(weapon_repository)
    try:
        await use_case.execute(
            query_factory.WeaponQueryFactory.query(st_weapon.weapon_id)
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters,count",
    [
        [dict(), 1],
        [{"search_by_name": st_weapon.name}, 1],
        [{"filter_by_kind_ids": [st_weapon.weapon_kind_id]}, 1],
        [{"filter_by_material_ids": [st_weapon.material_id]}, 1],
        [{"search_by_name": "random_name"}, 0],
        [{"filter_by_kind_ids": [uuid4()]}, 0],
        [{"filter_by_material_ids": [uuid4()]}, 0],
    ],
    ids=[
        "all",
        "one_search_by_name",
        "one_filter_by_kind_ids",
        "one_filter_by_material_ids",
        "zero_search_by_name",
        "zero_filter_by_kind_ids",
        "zero_filter_by_material_ids",
    ],
)
async def test_get_weapons_ok(weapon_repository, filters, count):
    await save_weapon(weapon_repository, st_weapon)
    use_case = GetWeaponsUseCase(weapon_repository)
    result = await use_case.execute(query_factory.WeaponQueryFactory.queries(**filters))
    assert len(result) == count
