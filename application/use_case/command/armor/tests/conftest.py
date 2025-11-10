import asyncio
from uuid import UUID, uuid4

import pytest
from adapters.repository.inmemory.armor import InMemoryArmorRepository
from adapters.repository.inmemory.user import InMemoryUserRepository
from application.dto.command.armor import ArmorClassCommand, CreateArmorCommand
from application.dto.command.coin import CoinCommand
from application.dto.command.weight import WeightCommand
from application.use_case.command.armor.create_armor import CreateArmorUseCase
from domain.armor.armor import Armor
from domain.armor.armor_class import ArmorClass
from domain.armor.armor_type import ArmorType
from domain.armor.service import ArmorService
from domain.coin import Coins, PieceType
from domain.modifier import Modifier
from domain.user.user import User
from domain.weight import Weight, WeightUnit

admin_uuid = uuid4()
not_admin_uuid = uuid4()


@pytest.fixture
def admin_user() -> UUID:
    return admin_uuid


@pytest.fixture
def not_admin_user() -> UUID:
    return not_admin_uuid


def armor_create_command_from_data(data: list) -> CreateArmorCommand:
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
def gen_create_armor_command(request) -> CreateArmorCommand:
    return armor_create_command_from_data(request.param)


@pytest.fixture
def gen_armor_create_use_case(request) -> CreateArmorUseCase:
    armor_repository = InMemoryArmorRepository()
    name = request.param[0]
    if len(name) > 0:
        armor = Armor(
            uuid4(),
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
