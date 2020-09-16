from hypothesis import given

from tests.utils import (BoundPortedVerticesPair,
                         are_bound_ported_maybe_edges_equal)
from . import strategies


@given(strategies.vertices_pairs)
def test_basic(pair: BoundPortedVerticesPair) -> None:
    bound, ported = pair

    assert are_bound_ported_maybe_edges_equal(bound.incident_edge,
                                              ported.incident_edge)
