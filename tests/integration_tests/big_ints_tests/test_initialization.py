from typing import List

from hypothesis import given

from tests.utils import (BoundBigInt,
                         PortedBigInt,
                         are_bound_ported_big_ints_equal)
from . import strategies


@given(strategies.signs, strategies.digits)
def test_basic(sign: int, digits: List[int]) -> None:
    bound, ported = BoundBigInt(sign, digits), PortedBigInt(sign, digits)

    assert are_bound_ported_big_ints_equal(bound, ported)
