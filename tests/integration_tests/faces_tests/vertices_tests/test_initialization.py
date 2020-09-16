from hypothesis import given

from tests.utils import (BoundPortedMaybeEdgesPair,
                         BoundVertex,
                         PortedVertex,
                         are_bound_ported_vertices_equal)
from . import strategies


@given(strategies.coordinates, strategies.coordinates,
       strategies.maybe_edges_pairs)
def test_basic(x: int, y: int, incident_edges_pair: BoundPortedMaybeEdgesPair
               ) -> None:
    bound_incident_edge, ported_incident_edge = incident_edges_pair
    bound, ported = (BoundVertex(x, y, bound_incident_edge),
                     PortedVertex(x, y, ported_incident_edge))

    assert are_bound_ported_vertices_equal(bound, ported)
