import pytest
from domain.error import DomainError
from domain.subclass_feature.feature import SubclassFeature


@pytest.mark.parametrize(
    "name, description, level, should_error",
    [
        ["name", "description", 1, False],
        ["", "description", 1, True],
        ["name", "", 1, True],
        ["name", "description", 0, True],
        ["name", "description", 21, True],
    ],
)
def test_create(gen_uuid, name, description, level, should_error):
    try:
        SubclassFeature(gen_uuid(), gen_uuid(), name, description, level, "")
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("исключение не было брошено")


@pytest.mark.parametrize(
    "gen_feature, new_level, should_error",
    [
        [["name", "description", 1], 2, False],
        [["name", "description", 1], 1, True],
        [["name", "description", 1], 0, True],
        [["name", "description", 1], 21, True],
    ],
    indirect=["gen_feature"],
)
def test_change_level(gen_feature, new_level, should_error):
    try:
        gen_feature.new_level(new_level)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert gen_feature.level() == new_level
