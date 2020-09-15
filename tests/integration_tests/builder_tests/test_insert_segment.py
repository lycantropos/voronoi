from hypothesis import given

from tests.utils import (BoundPortedBuildersPair,
                         are_bound_ported_builders_equal)
from . import strategies


@given(strategies.builders_pairs, strategies.coordinates,
       strategies.coordinates, strategies.coordinates, strategies.coordinates)
def test_basic(pair: BoundPortedBuildersPair,
               start_x: int,
               start_y: int,
               end_x: int,
               end_y: int) -> None:
    bound, ported = pair

    assert (bound.insert_segment(start_x, start_y, end_x, end_y)
            == ported.insert_segment(start_x, start_y, end_x, end_y))
    assert are_bound_ported_builders_equal(bound, ported)
