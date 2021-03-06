from hypothesis import given

from tests.integration_tests.hints import BoundPortedBigFloatsPair
from tests.integration_tests.utils import are_bound_ported_big_floats_equal
from . import strategies


@given(strategies.big_floats_pairs, strategies.non_zero_big_floats_pairs)
def test_basic(first_pair: BoundPortedBigFloatsPair,
               second_pair: BoundPortedBigFloatsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    bound_result = first_bound / second_bound
    ported_result = first_ported / second_ported

    assert are_bound_ported_big_floats_equal(bound_result, ported_result)
