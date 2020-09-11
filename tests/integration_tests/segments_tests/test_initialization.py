from hypothesis import given

from tests.utils import (BoundPortedPointsPair,
                         BoundSegment,
                         PortedSegment,
                         are_bound_ported_segments_equal)
from . import strategies


@given(strategies.points_pairs, strategies.points_pairs)
def test_basic(starts_pair: BoundPortedPointsPair,
               ends_pair: BoundPortedPointsPair) -> None:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    bound, ported = (BoundSegment(bound_start, bound_end),
                     PortedSegment(ported_start, ported_end))

    assert are_bound_ported_segments_equal(bound, ported)
