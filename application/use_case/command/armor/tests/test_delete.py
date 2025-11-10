from uuid import uuid4

import pytest
from application.dto.command.armor import DeleteArmorCommand
from domain.error import DomainError


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "armor_delete_use_case",
    ["name"],
    indirect=["armor_delete_use_case"],
)
async def test_armor_not_exists(armor_delete_use_case, admin_user):
    with pytest.raises(DomainError):
        await armor_delete_use_case.execute(
            DeleteArmorCommand(user_id=admin_user, armor_id=uuid4())
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "armor_delete_use_case",
    ["name"],
    indirect=["armor_delete_use_case"],
)
async def test_armor_exists(armor_delete_use_case, admin_user, armor_id):
    await armor_delete_use_case.execute(
        DeleteArmorCommand(user_id=admin_user, armor_id=armor_id)
    )
