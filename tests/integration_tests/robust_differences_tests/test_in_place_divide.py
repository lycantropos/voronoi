from hypothesis import given

from tests.utils import (BoundPortedRobustDifferencesPair,
                         BoundPortedRobustFloatsPair,
                         are_bound_ported_robust_differences_equal)
from . import strategies


@given(strategies.robust_differences_pairs, strategies.robust_floats_pairs)
def test_basic(pair: BoundPortedRobustDifferencesPair,
               robust_floats_pair: BoundPortedRobustFloatsPair) -> None:
    bound, ported = pair
    bound_robust_float, ported_robust_float = robust_floats_pair

    bound /= bound_robust_float
    ported /= ported_robust_float

    assert are_bound_ported_robust_differences_equal(bound, ported)
