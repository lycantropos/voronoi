from typing import List

from hypothesis import given

from tests.utils import (BoundBigInt,
                         PortedBigInt,
                         are_bound_ported_big_ints_equal)
from . import strategies


@given(strategies.digits, strategies.signs)
def test_basic(digits: List[int], sign: int) -> None:
    bound, ported = BoundBigInt(digits, sign), PortedBigInt(digits, sign)

    assert are_bound_ported_big_ints_equal(bound, ported)
