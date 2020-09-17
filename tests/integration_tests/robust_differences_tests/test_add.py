from hypothesis import given

from tests.utils import (BoundPortedRobustDifferencesPair,
                         are_bound_ported_robust_differences_equal)
from . import strategies


@given(strategies.robust_differences_pairs,
       strategies.robust_differences_pairs)
def test_basic(first_pair: BoundPortedRobustDifferencesPair,
               second_pair: BoundPortedRobustDifferencesPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    bound_result = first_bound + second_bound
    ported_result = first_ported + second_ported

    assert are_bound_ported_robust_differences_equal(bound_result,
                                                     ported_result)
