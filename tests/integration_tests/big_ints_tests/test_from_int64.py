from hypothesis import given

from tests.bind_tests.hints import BoundBigInt
from tests.integration_tests.utils import are_bound_ported_big_ints_equal
from tests.port_tests.hints import PortedBigInt
from . import strategies


@given(strategies.integers_64)
def test_basic(value: int) -> None:
    bound, ported = BoundBigInt(value), PortedBigInt.from_int64(value)

    assert are_bound_ported_big_ints_equal(bound, ported)
