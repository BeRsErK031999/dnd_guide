from uuid import uuid4

import pytest
from domain.subrace.feature import SubraceFeature
from domain.subrace.increase_modifier import SubraceIncreaseModifier
from domain.subrace.subrace import Subrace

const_uuid = uuid4()


@pytest.fixture
def static_uuid():
    return const_uuid


@pytest.fixture
def gen_uuid():
    return uuid4


@pytest.fixture
def gen_features(request) -> list[SubraceFeature]:
    return [SubraceFeature(feature[0], feature[1]) for feature in request.param]


@pytest.fixture
def gen_increase_modifiers(request) -> list[SubraceIncreaseModifier]:
    return [SubraceIncreaseModifier(p[0], p[1]) for p in request.param]


@pytest.fixture
def gen_subrace(gen_uuid, request) -> Subrace:
    name, description, increase_modifiers, features = request.param
    increase_modifiers = [
        SubraceIncreaseModifier(p[0], p[1]) for p in increase_modifiers
    ]
    features = [SubraceFeature(feature[0], feature[1]) for feature in features]
    return Subrace(
        gen_uuid(), gen_uuid(), name, description, increase_modifiers, features, ""
    )
