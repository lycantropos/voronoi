from hypothesis import given

from tests.bind_tests.hints import BoundDiagram
from tests.integration_tests.hints import (BoundPortedCellsListsPair,
                                           BoundPortedEdgesListsPair,
                                           BoundPortedVerticesListsPair)
from tests.integration_tests.utils import are_bound_ported_diagrams_equal
from tests.port_tests.hints import PortedDiagram
from . import strategies


@given(strategies.cells_lists_pairs, strategies.edges_lists_pairs,
       strategies.vertices_lists_pairs)
def test_basic(cells_pair: BoundPortedCellsListsPair,
               edges_pair: BoundPortedEdgesListsPair,
               vertices_pair: BoundPortedVerticesListsPair) -> None:
    bound_cells, ported_cells = cells_pair
    bound_edges, ported_edges = edges_pair
    bound_vertices, ported_vertices = vertices_pair
    bound, ported = (BoundDiagram(bound_cells, bound_edges, bound_vertices),
                     PortedDiagram(ported_cells, ported_edges,
                                   ported_vertices))

    assert are_bound_ported_diagrams_equal(bound, ported)
