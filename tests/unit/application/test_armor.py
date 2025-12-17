from uuid import uuid4

import pytest
from application.use_case.command.armor import (
    CreateArmorUseCase,
    DeleteArmorUseCase,
    UpdateArmorUseCase,
)
from application.use_case.query.armor import GetArmorsUseCase, GetArmorUseCase
from domain import error
from domain.armor.armor_type import ArmorType
from domain.armor.service import ArmorService
from domain.coin import PieceType
from domain.weight import WeightUnit
from tests.factories import command_factory, model_factory, query_factory

armor = model_factory.armor_model_factory()
user = model_factory.user_model_factory()


def armor_service(armor_repository):
    return ArmorService(armor_repository)


async def save_material(material_repository, material):
    await material_repository.save(material)


async def save_armor(armor_repository, armor):
    await armor_repository.save(armor)


async def save_user(user_repository, user):
    await user_repository.save(user)


@pytest.mark.asyncio
async def test_create_ok(armor_repository, material_repository, user_repository):
    await save_user(user_repository, user)
    material = model_factory.material_model_factory()
    await save_material(material_repository, material)
    use_case = CreateArmorUseCase(
        armor_service(armor_repository),
        user_repository,
        armor_repository,
        material_repository,
    )
    result = await use_case.execute(
        command_factory.ArmorCommandFactory.create(
            user_id=user.user_id, material_id=material.material_id
        )
    )
    assert result is not None


@pytest.mark.asyncio
async def test_create_material_not_exists(
    armor_repository, material_repository, user_repository
):
    await save_user(user_repository, user)
    use_case = CreateArmorUseCase(
        armor_service(armor_repository),
        user_repository,
        armor_repository,
        material_repository,
    )
    try:
        await use_case.execute(
            command_factory.ArmorCommandFactory.create(
                user_id=user.user_id, material_id=model_factory.uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("не было вызвано исключение")


@pytest.mark.asyncio
async def test_create_name_exists(
    armor_repository, material_repository, user_repository
):
    await save_user(user_repository, user)
    material = model_factory.material_model_factory()
    await save_material(material_repository, material)
    armor = model_factory.armor_model_factory(
        name="armor_name", material_id=material.material_id
    )
    await save_armor(armor_repository, armor)
    use_case = CreateArmorUseCase(
        armor_service(armor_repository),
        user_repository,
        armor_repository,
        material_repository,
    )
    try:
        await use_case.execute(
            command_factory.ArmorCommandFactory.create(
                user_id=user.user_id,
                name="armor_name",
                material_id=material.material_id,
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("не было вызвано исключение")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field",
    [
        {
            "user_id": user.user_id,
            "name": "new_armor_name",
            "model_name": "name",
            "new_value": "new_armor_name",
        },
        {
            "user_id": user.user_id,
            "description": "new_armor_description",
            "model_name": "description",
            "new_value": "new_armor_description",
        },
        {
            "user_id": user.user_id,
            "strength": 18,
            "model_name": "strength",
            "new_value": 18,
        },
        {
            "user_id": user.user_id,
            "stealth": False,
            "model_name": "stealth",
            "new_value": False,
        },
        {
            "user_id": user.user_id,
            "armor_type": ArmorType.LIGHT_ARMOR.name.lower(),
            "model_name": "armor_type",
            "new_value": ArmorType.LIGHT_ARMOR.name.lower(),
        },
        {
            "user_id": user.user_id,
            "armor_class": command_factory.armor_class_command(base_class=15),
            "model_name": "armor_class",
            "new_value": model_factory.armor_class_model_factory(base_class=15),
        },
        {
            "user_id": user.user_id,
            "armor_weight": command_factory.weight_command_factory(
                count=15, unit=WeightUnit.LB.name.lower()
            ),
            "model_name": "weight",
            "new_value": model_factory.weight_model_factory(
                count=15, unit=WeightUnit.LB.name.lower()
            ),
        },
        {
            "user_id": user.user_id,
            "cost": command_factory.coin_command_factory(
                count=20, piece_type=PieceType.COPPER.name.lower()
            ),
            "model_name": "cost",
            "new_value": model_factory.coins_model_factory(
                count=20, piece_type=PieceType.COPPER.name.lower()
            ),
        },
    ],
    ids=[
        "name",
        "description",
        "strength",
        "stealth",
        "armor_type",
        "armor_class",
        "weight",
        "cost",
    ],
)
async def test_update_ok(
    armor_repository, material_repository, user_repository, update_field
):
    await save_user(user_repository, user)
    material = model_factory.material_model_factory()
    await save_material(material_repository, material)
    armor = model_factory.armor_model_factory(material_id=material.material_id)
    await save_armor(armor_repository, armor)
    use_case = UpdateArmorUseCase(
        armor_service(armor_repository),
        user_repository,
        armor_repository,
        material_repository,
    )
    model_field_name = update_field.pop("model_name")
    new_value = update_field.pop("new_value")
    result = await use_case.execute(
        command_factory.ArmorCommandFactory.update(
            armor_id=armor.armor_id, **update_field
        )
    )
    assert result is None
    updated_armor = await armor_repository.get_by_id(armor.armor_id)
    assert updated_armor is not None
    assert getattr(updated_armor, model_field_name) == new_value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_field",
    [
        {
            "user_id": user.user_id,
            "armor_id": armor.armor_id,
            "armor_class": command_factory.armor_class_command(
                base_class=armor.armor_class.base_class,
                modifier=armor.armor_class.modifier,
                max_modifier_bonus=armor.armor_class.max_modifier_bonus,
            ),
            "error_status": error.DomainErrorStatus.IDEMPOTENT,
        },
        {
            "user_id": user.user_id,
            "armor_id": armor.armor_id,
            "armor_weight": command_factory.weight_command_factory(
                count=armor.weight.count, unit=armor.weight.unit
            ),
            "error_status": error.DomainErrorStatus.IDEMPOTENT,
        },
        {
            "user_id": user.user_id,
            "armor_id": armor.armor_id,
            "cost": command_factory.coin_command_factory(
                count=armor.cost.count, piece_type=armor.cost.piece_type
            ),
            "error_status": error.DomainErrorStatus.IDEMPOTENT,
        },
        {
            "user_id": user.user_id,
            "armor_id": uuid4(),
            "name": "new_armor_name",
            "error_status": error.DomainErrorStatus.NOT_FOUND,
        },
        {
            "user_id": user.user_id,
            "armor_id": armor.armor_id,
            "armor_type": armor.armor_type,
            "error_status": error.DomainErrorStatus.IDEMPOTENT,
        },
        {
            "user_id": user.user_id,
            "armor_id": armor.armor_id,
            "name": armor.name,
            "error_status": error.DomainErrorStatus.INVALID_DATA,
        },
        {
            "user_id": user.user_id,
            "armor_id": armor.armor_id,
            "strength": armor.strength,
            "error_status": error.DomainErrorStatus.IDEMPOTENT,
        },
        {
            "user_id": user.user_id,
            "armor_id": armor.armor_id,
            "stealth": armor.stealth,
            "error_status": error.DomainErrorStatus.IDEMPOTENT,
        },
        {
            "user_id": user.user_id,
            "armor_id": armor.armor_id,
            "material_id": uuid4(),
            "error_status": error.DomainErrorStatus.INVALID_DATA,
        },
        {
            "user_id": user.user_id,
            "armor_id": armor.armor_id,
            "material_id": armor.material_id,
            "error_status": error.DomainErrorStatus.INVALID_DATA,
        },
        {
            "user_id": user.user_id,
            "armor_id": uuid4(),
            "error_status": error.DomainErrorStatus.INVALID_DATA,
        },
    ],
    ids=[
        "armor_class",
        "weight",
        "cost",
        "not_found",
        "armor_type",
        "name",
        "strength",
        "stealth",
        "material_not_exists",
        "material_no_change",
        "no_data",
    ],
)
async def test_update_fail(
    armor_repository, material_repository, user_repository, update_field
):
    await save_user(user_repository, user)
    material = model_factory.material_model_factory()
    await save_material(material_repository, material)
    armor = model_factory.armor_model_factory(material_id=material.material_id)
    await save_armor(armor_repository, armor)
    use_case = UpdateArmorUseCase(
        armor_service(armor_repository),
        user_repository,
        armor_repository,
        material_repository,
    )
    error_status = update_field.pop("error_status")
    try:
        result = await use_case.execute(
            command_factory.ArmorCommandFactory.update(**update_field)
        )
    except error.DomainError as e:
        assert e.status == error_status
        return
    pytest.fail("не было вызвано исключение")


@pytest.mark.asyncio
async def test_delete_ok(armor_repository, material_repository, user_repository):
    await save_user(user_repository, user)
    material = model_factory.material_model_factory()
    await save_material(material_repository, material)
    armor = model_factory.armor_model_factory(material_id=material.material_id)
    await save_armor(armor_repository, armor)
    use_case = DeleteArmorUseCase(
        user_repository,
        armor_repository,
    )
    result = await use_case.execute(
        command_factory.ArmorCommandFactory.delete(
            user_id=user.user_id, armor_id=armor.armor_id
        )
    )
    assert result is None
    if await armor_repository.id_exists(armor.armor_id):
        pytest.fail("доспехи не были удалены")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "delete_field",
    [
        {
            "user_id": user.user_id,
            "armor_id": uuid4(),
            "error_status": error.DomainErrorStatus.NOT_FOUND,
        },
    ],
    ids=[
        "not_found",
    ],
)
async def test_delete_fail(
    armor_repository, material_repository, user_repository, delete_field
):
    await save_user(user_repository, user)
    material = model_factory.material_model_factory()
    await save_material(material_repository, material)
    armor = model_factory.armor_model_factory(material_id=material.material_id)
    await save_armor(armor_repository, armor)
    use_case = DeleteArmorUseCase(
        user_repository,
        armor_repository,
    )
    error_status = delete_field.pop("error_status")
    try:
        result = await use_case.execute(
            command_factory.ArmorCommandFactory.delete(**delete_field)
        )
    except error.DomainError as e:
        assert e.status == error_status
        return
    pytest.fail("не было вызвано исключение")


@pytest.mark.asyncio
async def test_get_armor_ok(armor_repository, material_repository):
    material = model_factory.material_model_factory()
    await save_material(material_repository, material)
    armor = model_factory.armor_model_factory(material_id=material.material_id)
    await save_armor(armor_repository, armor)
    use_case = GetArmorUseCase(
        armor_repository,
    )
    result = await use_case.execute(
        query_factory.ArmorQueryFactory.query(armor_id=armor.armor_id)
    )
    assert result is not None
    assert result.armor_id == armor.armor_id


@pytest.mark.asyncio
async def test_get_armor_fail(armor_repository, material_repository):
    material = model_factory.material_model_factory()
    await save_material(material_repository, material)
    armor = model_factory.armor_model_factory(material_id=material.material_id)
    await save_armor(armor_repository, armor)
    use_case = GetArmorUseCase(
        armor_repository,
    )
    try:
        result = await use_case.execute(
            query_factory.ArmorQueryFactory.query(armor_id=uuid4())
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("не было вызвано исключение")


@pytest.mark.asyncio
async def test_get_armors_ok(armor_repository, material_repository):
    material = model_factory.material_model_factory()
    await save_material(material_repository, material)
    armor = model_factory.armor_model_factory(material_id=material.material_id)
    armor2 = model_factory.armor_model_factory(
        name="Second Armor", material_id=material.material_id
    )
    await save_armor(armor_repository, armor)
    await save_armor(armor_repository, armor2)
    use_case = GetArmorsUseCase(
        armor_repository,
    )
    result = await use_case.execute(
        query_factory.ArmorQueryFactory.queries(search_by_name=armor2.name)
    )
    assert result is not None
    assert result[0].armor_id == armor.armor_id
