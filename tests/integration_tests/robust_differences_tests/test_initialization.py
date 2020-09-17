from hypothesis import given

from tests.utils import (BoundPortedRobustFloatsPair,
                         BoundRobustDifference,
                         PortedRobustDifference,
                         are_bound_ported_robust_differences_equal)
from . import strategies


@given(strategies.robust_floats_pairs, strategies.robust_floats_pairs)
def test_basic(minuends_pair: BoundPortedRobustFloatsPair,
               subtrahends_pair: BoundPortedRobustFloatsPair) -> None:
    bound_minuend, ported_minuend = minuends_pair
    bound_subtrahend, ported_subtrahend = subtrahends_pair
    bound, ported = (BoundRobustDifference(bound_minuend, bound_subtrahend),
                     PortedRobustDifference(ported_minuend, ported_subtrahend))

    assert are_bound_ported_robust_differences_equal(bound, ported)
