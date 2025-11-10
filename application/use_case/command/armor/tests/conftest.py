import asyncio
from uuid import UUID, uuid4

import pytest
from adapters.repository.inmemory import InMemoryArmorRepository, InMemoryUserRepository
from application.dto.command.armor import (
    ArmorClassCommand,
    CreateArmorCommand,
    UpdateArmorCommand,
)
from application.dto.command.coin import CoinCommand
from application.dto.command.weight import WeightCommand
from application.use_case.command.armor import (
    CreateArmorUseCase,
    DeleteArmorUseCase,
    UpdateArmorUseCase,
)
from domain.armor import Armor, ArmorClass, ArmorService, ArmorType
from domain.coin import Coins, PieceType
from domain.modifier import Modifier
from domain.user import User
from domain.weight import Weight, WeightUnit

admin_uuid = uuid4()
not_admin_uuid = uuid4()
armor_uuid = uuid4()


@pytest.fixture
def admin_user() -> UUID:
    return admin_uuid


@pytest.fixture
def armor_id() -> UUID:
    return armor_uuid


@pytest.fixture
def not_admin_user() -> UUID:
    return not_admin_uuid


@pytest.fixture
def create_armor_command(request) -> CreateArmorCommand:
    data = request.param
    if data[0]:
        return CreateArmorCommand(
            admin_uuid,
            data[1],
            data[2],
            data[3],
            ArmorClassCommand(data[4][0], data[4][1], data[4][2]),
            data[5],
            data[6],
            WeightCommand(data[7][0], data[7][1]),
            CoinCommand(data[8][0], data[8][1]),
        )
    return CreateArmorCommand(
        not_admin_uuid,
        data[1],
        data[2],
        data[3],
        ArmorClassCommand(data[4][0], data[4][1], data[4][2]),
        data[5],
        data[6],
        WeightCommand(data[7][0], data[7][1]),
        CoinCommand(data[8][0], data[8][1]),
    )


@pytest.fixture
def armor_create_use_case(request) -> CreateArmorUseCase:
    armor_repository = InMemoryArmorRepository()
    name = request.param[0]
    if len(name) > 0:
        armor = Armor(
            armor_uuid,
            ArmorType.HEAVY_ARMOR,
            name,
            "description",
            ArmorClass(10, Modifier.DEXTERITY, 2),
            0,
            True,
            Weight(20, WeightUnit.LB),
            Coins(20, PieceType.GOLD),
        )
        asyncio.run(armor_repository.save(armor))
    user_repository = InMemoryUserRepository()
    asyncio.run(user_repository.save(User(admin_uuid)))
    return CreateArmorUseCase(
        ArmorService(armor_repository), user_repository, armor_repository
    )


@pytest.fixture
def update_armor_command(request) -> UpdateArmorCommand:
    data = request.param
    if data[0]:
        return UpdateArmorCommand(
            admin_uuid,
            armor_uuid,
            data[1],
            data[2],
            data[3],
            (
                ArmorClassCommand(data[4][0], data[4][1], data[4][2])
                if data[4] is not None
                else None
            ),
            data[5],
            data[6],
            WeightCommand(data[7][0], data[7][1]) if data[7] is not None else None,
            CoinCommand(data[8][0], data[8][1]) if data[8] is not None else None,
        )
    return UpdateArmorCommand(
        not_admin_uuid,
        armor_uuid,
        data[1],
        data[2],
        data[3],
        (
            ArmorClassCommand(data[4][0], data[4][1], data[4][2])
            if data[4] is not None
            else None
        ),
        data[5],
        data[6],
        WeightCommand(data[7][0], data[7][1]) if data[7] is not None else None,
        CoinCommand(data[8][0], data[8][1]) if data[8] is not None else None,
    )


@pytest.fixture
def armor_update_use_case(request) -> UpdateArmorUseCase:
    armor_repository = InMemoryArmorRepository()
    name = request.param[0]
    if len(name) > 0:
        armor = Armor(
            armor_uuid,
            ArmorType.HEAVY_ARMOR,
            name,
            "description",
            ArmorClass(10, Modifier.DEXTERITY, 2),
            0,
            True,
            Weight(20, WeightUnit.LB),
            Coins(20, PieceType.GOLD),
        )
        asyncio.run(armor_repository.save(armor))
    user_repository = InMemoryUserRepository()
    asyncio.run(user_repository.save(User(admin_uuid)))
    return UpdateArmorUseCase(
        ArmorService(armor_repository), user_repository, armor_repository
    )


@pytest.fixture
def armor_delete_use_case(request) -> DeleteArmorUseCase:
    armor_repository = InMemoryArmorRepository()
    name = request.param[0]
    if len(name) > 0:
        armor = Armor(
            armor_uuid,
            ArmorType.HEAVY_ARMOR,
            name,
            "description",
            ArmorClass(10, Modifier.DEXTERITY, 2),
            0,
            True,
            Weight(20, WeightUnit.LB),
            Coins(20, PieceType.GOLD),
        )
        asyncio.run(armor_repository.save(armor))
    user_repository = InMemoryUserRepository()
    asyncio.run(user_repository.save(User(admin_uuid)))
    return DeleteArmorUseCase(user_repository, armor_repository)
