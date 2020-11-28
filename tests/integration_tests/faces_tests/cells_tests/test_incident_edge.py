from hypothesis import given

from tests.integration_tests.hints import BoundPortedCellsPair
from tests.integration_tests.utils import are_bound_ported_maybe_edges_equal
from . import strategies


@given(strategies.cells_pairs)
def test_basic(pair: BoundPortedCellsPair) -> None:
    bound, ported = pair

    assert are_bound_ported_maybe_edges_equal(bound.incident_edge,
                                              ported.incident_edge)
