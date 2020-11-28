from hypothesis import given

from tests.integration_tests.hints import BoundPortedBigIntsPair
from tests.integration_tests.utils import are_bound_ported_big_ints_equal
from . import strategies


@given(strategies.big_ints_pairs)
def test_basic(pair: BoundPortedBigIntsPair) -> None:
    bound, ported = pair

    assert are_bound_ported_big_ints_equal(-bound, -ported)
