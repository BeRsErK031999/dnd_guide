import pytest
from domain.error import DomainError
from domain.modifier import Modifier
from domain.subrace.subrace import Subrace


@pytest.mark.parametrize(
    "name, description, gen_increase_modifiers, gen_features, should_error",
    [
        [
            "name",
            "description",
            [[Modifier.CHARISMA, 2]],
            [
                ["feature_name", "feature_description"],
                ["feature2_name", "feature2_description"],
            ],
            False,
        ],
        [
            "",
            "description",
            [[Modifier.CHARISMA, 2]],
            [
                ["feature_name", "feature_description"],
                ["feature2_name", "feature2_description"],
            ],
            True,
        ],
        [
            "name",
            "",
            [[Modifier.CHARISMA, 2]],
            [
                ["feature_name", "feature_description"],
                ["feature2_name", "feature2_description"],
            ],
            True,
        ],
        [
            "name",
            "description",
            [[Modifier.CHARISMA, 2], [Modifier.CHARISMA, 2]],
            [
                ["feature_name", "feature_description"],
                ["feature2_name", "feature2_description"],
            ],
            True,
        ],
        [
            "name",
            "description",
            [[Modifier.CHARISMA, 2]],
            [
                ["feature_name", "feature_description"],
                ["feature2_name", "feature2_description"],
                ["feature_name", "feature_description"],
                ["feature2_name", "feature2_description"],
            ],
            True,
        ],
    ],
    indirect=["gen_features", "gen_increase_modifiers"],
)
def test_create(
    gen_uuid, name, description, gen_increase_modifiers, gen_features, should_error
):
    try:
        Subrace(
            gen_uuid(),
            gen_uuid(),
            name,
            description,
            gen_increase_modifiers,
            gen_features,
        )
    except DomainError as e:
        if should_error:
            return
        raise e
    if should_error:
        pytest.fail("исключение не было брошено")


@pytest.mark.parametrize(
    "gen_subrace, gen_increase_modifiers, should_error",
    [
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [[Modifier.CONSTITUTION, 2]],
            False,
        ],
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [],
            False,
        ],
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [[Modifier.CHARISMA, 2]],
            True,
        ],
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [[Modifier.CONSTITUTION, 2], [Modifier.CHARISMA, 2]],
            False,
        ],
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [[Modifier.CONSTITUTION, 2], [Modifier.CONSTITUTION, 2]],
            True,
        ],
    ],
    indirect=["gen_subrace", "gen_increase_modifiers"],
)
def test_change_increase_modifier(gen_subrace, gen_increase_modifiers, should_error):
    try:
        gen_subrace.new_increase_modifiers(gen_increase_modifiers)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert gen_subrace.increase_modifiers() == gen_increase_modifiers


@pytest.mark.parametrize(
    "gen_subrace, gen_features, should_error",
    [
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [["feature_new", "new"]],
            False,
        ],
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [],
            False,
        ],
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [["feature_name", "feature_description"]],
            True,
        ],
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [["feature_name", "feature_description"], ["feature_new", "new"]],
            False,
        ],
        [
            [
                "name",
                "description",
                [[Modifier.CHARISMA, 2]],
                [["feature_name", "feature_description"]],
            ],
            [
                ["feature_name", "feature_description"],
                ["feature_name", "feature_description"],
            ],
            True,
        ],
    ],
    indirect=["gen_subrace", "gen_features"],
)
def test_change_features(gen_subrace, gen_features, should_error):
    try:
        gen_subrace.new_features(gen_features)
    except DomainError as e:
        if should_error:
            return
        raise e
    assert gen_subrace.features() == gen_features
