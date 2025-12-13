from uuid import uuid4

import pytest
from application.use_case.command.feat import (
    CreateFeatUseCase,
    DeleteFeatUseCase,
    UpdateFeatUseCase,
)
from application.use_case.query.feat import GetFeatsUseCase, GetFeatUseCase
from domain import error
from domain.armor.armor_type import ArmorType
from domain.feat import FeatService
from domain.modifier import Modifier
from tests.factories import command_factory, model_factory, query_factory

st_user = model_factory.user_model_factory()
st_feat = model_factory.feat_model_factory()


def feat_service(feat_repository):
    return FeatService(feat_repository)


async def save_user(user_repository, user):
    await user_repository.create(user)


async def save_feat(feat_repository, feat):
    await feat_repository.create(feat)


@pytest.mark.asyncio
async def test_create_ok(user_repository, feat_repository):
    await save_user(user_repository, st_user)
    use_case = CreateFeatUseCase(
        feat_service(feat_repository), user_repository, feat_repository
    )
    result = await use_case.execute(
        command_factory.FeatCommandFactory.create(user_id=st_user.user_id)
    )
    assert await feat_repository.id_exists(result)


@pytest.mark.asyncio
async def test_create_name_exists(user_repository, feat_repository):
    await save_user(user_repository, st_user)
    await save_feat(feat_repository, st_feat)
    use_case = CreateFeatUseCase(
        feat_service(feat_repository), user_repository, feat_repository
    )
    try:
        await use_case.execute(
            command_factory.FeatCommandFactory.create(
                user_id=st_user.user_id, name=st_feat.name
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
        [{"name": "new_name"}, {"name": "new_name"}],
        [{"description": "new_name"}, {"description": "new_name"}],
        [{"caster": True}, {"caster": True}],
        [
            {"required_armor_types": [ArmorType.LIGHT_ARMOR.name.lower()]},
            {"required_armor_types": [ArmorType.LIGHT_ARMOR.name.lower()]},
        ],
        [
            {
                "required_modifiers": [
                    command_factory.feat_required_modifier_command_factory(
                        modifier=Modifier.DEXTERITY.name.lower(), min_value=10
                    )
                ]
            },
            {
                "required_modifiers": [
                    model_factory.feat_required_modifier_model_factory(
                        modifier=Modifier.DEXTERITY.name.lower(), min_value=10
                    )
                ]
            },
        ],
        [
            {"increase_modifiers": [Modifier.STRENGTH.name.lower()]},
            {"increase_modifiers": [Modifier.STRENGTH.name.lower()]},
        ],
    ],
    ids=[
        "name",
        "description",
        "caster",
        "required_armor_types",
        "required_modifiers",
        "increase_modifiers",
    ],
)
async def test_update_ok(user_repository, feat_repository, update_field, checked):
    await save_user(user_repository, st_user)
    await save_feat(feat_repository, st_feat)
    use_case = UpdateFeatUseCase(
        feat_service(feat_repository), user_repository, feat_repository
    )
    await use_case.execute(
        command_factory.FeatCommandFactory.update(
            user_id=st_user.user_id, feat_id=st_feat.feat_id, **update_field
        )
    )
    feat = await feat_repository.get_by_id(st_feat.feat_id)
    assert getattr(feat, list(checked.keys())[0]) == list(checked.values())[0]


@pytest.mark.asyncio
async def test_update_feat_not_exists(user_repository, feat_repository):
    await save_user(user_repository, st_user)
    use_case = UpdateFeatUseCase(
        feat_service(feat_repository), user_repository, feat_repository
    )
    try:
        await use_case.execute(
            command_factory.FeatCommandFactory.update(
                user_id=st_user.user_id, feat_id=uuid4(), name="random_name"
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_update_feat_name_exists(user_repository, feat_repository):
    await save_user(user_repository, st_user)
    await save_feat(feat_repository, st_feat)
    exists_feat = model_factory.feat_model_factory(feat_id=uuid4(), name="random")
    await save_feat(feat_repository, exists_feat)
    use_case = UpdateFeatUseCase(
        feat_service(feat_repository), user_repository, feat_repository
    )
    try:
        await use_case.execute(
            command_factory.FeatCommandFactory.update(
                user_id=st_user.user_id, feat_id=st_feat.feat_id, name=exists_feat.name
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_delete_ok(user_repository, feat_repository):
    await save_user(user_repository, st_user)
    await save_feat(feat_repository, st_feat)
    use_case = DeleteFeatUseCase(user_repository, feat_repository)
    await use_case.execute(
        command_factory.FeatCommandFactory.delete(
            user_id=st_user.user_id, feat_id=st_feat.feat_id
        )
    )
    assert not await feat_repository.id_exists(st_feat.feat_id)


@pytest.mark.asyncio
async def test_delete_feat_not_exists(user_repository, feat_repository):
    await save_user(user_repository, st_user)
    await save_feat(feat_repository, st_feat)
    use_case = DeleteFeatUseCase(user_repository, feat_repository)
    try:
        await use_case.execute(
            command_factory.FeatCommandFactory.delete(
                user_id=st_user.user_id, feat_id=uuid4()
            )
        )
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
async def test_get_feat_ok(user_repository, feat_repository):
    await save_user(user_repository, st_user)
    await save_feat(feat_repository, st_feat)
    use_case = GetFeatUseCase(feat_repository)
    result = await use_case.execute(
        query_factory.FeatQueryFactory.query(feat_id=st_feat.feat_id)
    )
    assert result == st_feat


@pytest.mark.asyncio
async def test_get_feat_not_exists(user_repository, feat_repository):
    await save_user(user_repository, st_user)
    use_case = GetFeatUseCase(feat_repository)
    try:
        await use_case.execute(query_factory.FeatQueryFactory.query(feat_id=uuid4()))
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.NOT_FOUND
        return
    pytest.fail("not raised exception")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter,count",
    [
        [{"search_by_name": st_feat.name}, 1],
        [{"search_by_name": "random_name"}, 0],
        [dict(), 1],
    ],
    ids=["one", "zero", "all"],
)
async def test_get_feats_ok(user_repository, feat_repository, filter, count):
    await save_user(user_repository, st_user)
    await save_feat(feat_repository, st_feat)
    use_case = GetFeatsUseCase(feat_repository)
    result = await use_case.execute(query_factory.FeatQueryFactory.queries(**filter))
    assert len(result) == count
