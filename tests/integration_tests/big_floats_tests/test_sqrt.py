from hypothesis import given

from tests.utils import (BoundPortedBigFloatsPair,
                         are_bound_ported_big_floats_equal)
from . import strategies


@given(strategies.big_floats_pairs)
def test_basic(pair: BoundPortedBigFloatsPair) -> None:
    bound, ported = pair

    bound_result = bound.sqrt()
    ported_result = ported.sqrt()

    assert are_bound_ported_big_floats_equal(bound_result, ported_result)
