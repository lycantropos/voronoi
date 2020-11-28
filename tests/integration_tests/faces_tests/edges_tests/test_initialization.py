from hypothesis import given

from tests.bind_tests.hints import BoundEdge
from tests.integration_tests.hints import (BoundPortedCellsPair,
                                           BoundPortedVerticesPair)
from tests.integration_tests.utils import are_bound_ported_edges_equal
from tests.port_tests.hints import PortedEdge
from . import strategies


@given(strategies.maybe_vertices_pairs, strategies.cells_pairs,
       strategies.booleans, strategies.booleans)
def test_basic(starts_pair: BoundPortedVerticesPair,
               cells_pair: BoundPortedCellsPair,
               is_linear: bool,
               is_primary: bool) -> None:
    bound_start, ported_start = starts_pair
    bound_cell, ported_cell = cells_pair

    bound, ported = (BoundEdge(bound_start, bound_cell, is_linear, is_primary),
                     PortedEdge(ported_start, ported_cell, is_linear,
                                is_primary))

    assert are_bound_ported_edges_equal(bound, ported)
