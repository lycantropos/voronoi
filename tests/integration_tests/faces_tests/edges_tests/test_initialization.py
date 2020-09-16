from hypothesis import given

from tests.utils import (BoundEdge,
                         BoundPortedPointsPair,
                         PortedEdge,
                         are_bound_ported_edges_equal)
from . import strategies


@given(strategies.points_pairs, strategies.points_pairs)
def test_basic(starts_pair: BoundPortedPointsPair,
               ends_pair: BoundPortedPointsPair) -> None:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    bound, ported = (BoundEdge(bound_start, bound_end),
                     PortedEdge(ported_start, ported_end))

    assert are_bound_ported_edges_equal(bound, ported)
