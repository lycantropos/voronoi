from hypothesis import given

from tests.utils import (BoundEdge,
                         BoundPortedMaybeCellsPair,
                         BoundPortedMaybeEdgesPair,
                         BoundPortedVerticesPair,
                         PortedEdge,
                         are_bound_ported_edges_equal)
from . import strategies


@given(strategies.maybe_vertices_pairs, strategies.maybe_edges_pairs,
       strategies.maybe_edges_pairs, strategies.maybe_edges_pairs,
       strategies.maybe_cells_pairs, strategies.booleans, strategies.booleans)
def test_basic(starts_pair: BoundPortedVerticesPair,
               twins_pair: BoundPortedMaybeEdgesPair,
               prev_edges_pair: BoundPortedMaybeEdgesPair,
               next_edges_pair: BoundPortedMaybeEdgesPair,
               cells_pair: BoundPortedMaybeCellsPair,
               is_linear: bool,
               is_primary: bool) -> None:
    bound_start, ported_start = starts_pair
    bound_twin, ported_twin = twins_pair
    bound_prev, ported_prev = prev_edges_pair
    bound_next, ported_next = next_edges_pair
    bound_cell, ported_cell = cells_pair
    bound, ported = (BoundEdge(bound_start, bound_twin, bound_prev, bound_next,
                               bound_cell, is_linear, is_primary),
                     PortedEdge(ported_start, ported_twin, ported_prev,
                                ported_next, ported_cell, is_linear,
                                is_primary))

    assert are_bound_ported_edges_equal(bound, ported)
