from _voronoi import robust_product_with_sqrt as bound
from hypothesis import given

from tests.integration_tests.hints import BoundPortedBigIntsPair
from tests.integration_tests.utils import are_bound_ported_big_floats_equal
from voronoi.big_int import robust_product_with_sqrt as ported
from . import strategies


@given(strategies.big_ints_pairs, strategies.non_negative_big_ints_pairs)
def test_basic(first_pair: BoundPortedBigIntsPair,
               second_pair: BoundPortedBigIntsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    bound_result = bound(first_bound, second_bound)
    ported_result = ported(first_ported, second_ported)

    assert are_bound_ported_big_floats_equal(bound_result, ported_result)
