from uuid import uuid4

import pytest
from domain.subclass_feature.feature import SubclassFeature


@pytest.fixture
def gen_uuid():
    return uuid4


@pytest.fixture
def gen_feature(gen_uuid, request) -> SubclassFeature:
    name, description, level = request.param
    return SubclassFeature(gen_uuid(), gen_uuid(), name, description, level)
