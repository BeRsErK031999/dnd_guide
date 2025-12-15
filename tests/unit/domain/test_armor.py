import pytest
from domain import armor, error
from tests.factories import domain_factory


def test_create_ok():
    domain_factory.armor_factory()


@pytest.mark.parametrize(
    "fields",
    [{"strength": -1}, {"strength": 21}],
    ids=["strength_is_0", "strength_is_21"],
)
def test_create_invalid(fields):
    try:
        domain_factory.armor_factory(**fields)
    except error.DomainError as e:
        assert e.status == error.DomainErrorStatus.INVALID_DATA
        return
    pytest.fail("not raised exception")
