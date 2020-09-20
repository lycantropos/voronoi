from _voronoi import (to_second_point_segment_segment_quadruplets_expression
                      as bound)
from hypothesis import given

from tests.utils import (BoundPortedBigIntsQuadrupletsPair,
                         are_bound_ported_big_floats_equal)
from voronoi.big_int import (
    to_second_point_segment_segment_quadruplets_expression as ported)
from . import strategies


@given(strategies.big_ints_pairs_quadruplets,
       strategies.non_negative_big_ints_pairs_quadruplets)
def test_basic(first_pair: BoundPortedBigIntsQuadrupletsPair,
               second_pair: BoundPortedBigIntsQuadrupletsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    bound_result = bound(first_bound, second_bound)
    ported_result = ported(first_ported, second_ported)

    assert are_bound_ported_big_floats_equal(bound_result, ported_result)
