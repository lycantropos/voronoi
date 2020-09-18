from hypothesis import given

from tests.utils import (BoundPortedBigIntsPair,
                         are_bound_ported_big_ints_equal)
from . import strategies


@given(strategies.big_ints_pairs)
def test_basic(pair: BoundPortedBigIntsPair) -> None:
    bound, ported = pair

    assert are_bound_ported_big_ints_equal(-bound, -ported)
