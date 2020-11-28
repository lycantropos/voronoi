from hypothesis import given

from tests.integration_tests.hints import (
    BoundPortedRobustDifferencesOrFloatsPair,
    BoundPortedRobustDifferencesPair)
from tests.integration_tests.utils import (
    are_bound_ported_robust_differences_equal)
from . import strategies


@given(strategies.robust_differences_pairs,
       strategies.robust_floats_or_differences_pairs)
def test_basic(first_pair: BoundPortedRobustDifferencesPair,
               second_pair: BoundPortedRobustDifferencesOrFloatsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    first_bound *= second_bound
    first_ported *= second_ported

    assert are_bound_ported_robust_differences_equal(first_bound, first_ported)
