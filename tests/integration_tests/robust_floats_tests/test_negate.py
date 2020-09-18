from hypothesis import given

from tests.utils import (BoundPortedRobustFloatsPair,
                         are_bound_ported_robust_floats_equal)
from . import strategies


@given(strategies.robust_floats_pairs)
def test_basic(pair: BoundPortedRobustFloatsPair) -> None:
    bound, ported = pair

    assert are_bound_ported_robust_floats_equal(-bound, -ported)