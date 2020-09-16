from hypothesis import given

from tests.utils import (BoundDiagram,
                         BoundPortedCellsListsPair,
                         BoundPortedEdgesListsPair,
                         BoundPortedVerticesListsPair,
                         PortedDiagram,
                         are_bound_ported_diagrams_equal)
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
