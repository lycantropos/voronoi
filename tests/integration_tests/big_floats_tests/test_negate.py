from hypothesis import given

from tests.integration_tests.hints import BoundPortedBigFloatsPair
from tests.integration_tests.utils import are_bound_ported_big_floats_equal
from . import strategies


@given(strategies.big_floats_pairs)
def test_basic(pair: BoundPortedBigFloatsPair) -> None:
    bound, ported = pair

    assert are_bound_ported_big_floats_equal(-bound, -ported)
