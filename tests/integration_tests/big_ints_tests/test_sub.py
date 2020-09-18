from hypothesis import given

from tests.utils import (BoundPortedBigIntsPair,
                         are_bound_ported_big_ints_equal)
from . import strategies


@given(strategies.big_ints_pairs, strategies.big_ints_pairs)
def test_basic(first_pair: BoundPortedBigIntsPair,
               second_pair: BoundPortedBigIntsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    bound_result = first_bound - second_bound
    ported_result = first_ported - second_ported

    assert are_bound_ported_big_ints_equal(bound_result, ported_result)
