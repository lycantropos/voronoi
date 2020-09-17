from hypothesis import given

from tests.utils import (BoundPortedRobustFloatsPair,
                         are_bound_ported_robust_floats_equal)
from . import strategies


@given(strategies.robust_floats_pairs, strategies.robust_floats_pairs)
def test_basic(first_pair: BoundPortedRobustFloatsPair,
               second_pair: BoundPortedRobustFloatsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert are_bound_ported_robust_floats_equal(first_bound + second_bound,
                                                first_ported + second_ported)
