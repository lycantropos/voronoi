from hypothesis import given

from tests.integration_tests.hints import BoundPortedEdgesPair
from tests.integration_tests.utils import are_bound_ported_maybe_edges_equal
from . import strategies


@given(strategies.edges_pairs)
def test_basic(pair: BoundPortedEdgesPair) -> None:
    bound, ported = pair

    assert are_bound_ported_maybe_edges_equal(bound.rot_prev, ported.rot_prev)
