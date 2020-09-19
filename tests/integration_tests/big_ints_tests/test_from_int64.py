from hypothesis import given

from tests.utils import (BoundBigInt,
                         PortedBigInt,
                         are_bound_ported_big_ints_equal)
from . import strategies


@given(strategies.integers_64)
def test_basic(value: int) -> None:
    bound, ported = BoundBigInt(value), PortedBigInt.from_int64(value)

    assert are_bound_ported_big_ints_equal(bound, ported)
