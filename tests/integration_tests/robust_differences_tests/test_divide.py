from hypothesis import given

from tests.integration_tests.hints import (BoundPortedRobustDifferencesPair,
                                           BoundPortedRobustFloatsPair)
from tests.integration_tests.utils import (
    are_bound_ported_robust_differences_equal)
from . import strategies


@given(strategies.robust_differences_pairs, strategies.robust_floats_pairs)
def test_basic(pair: BoundPortedRobustDifferencesPair,
               robust_floats_pair: BoundPortedRobustFloatsPair) -> None:
    bound, ported = pair
    bound_robust_float, ported_robust_float = robust_floats_pair

    bound_result = bound / bound_robust_float
    ported_result = ported / ported_robust_float

    assert are_bound_ported_robust_differences_equal(bound_result,
                                                     ported_result)
