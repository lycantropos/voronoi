from hypothesis import given

from tests.integration_tests.hints import BoundPortedRobustDifferencesPair
from tests.integration_tests.utils import are_bound_ported_robust_floats_equal
from . import strategies


@given(strategies.robust_differences_pairs)
def test_basic(pair: BoundPortedRobustDifferencesPair) -> None:
    bound, ported = pair

    assert are_bound_ported_robust_floats_equal(bound.evaluate(),
                                                ported.evaluate())
