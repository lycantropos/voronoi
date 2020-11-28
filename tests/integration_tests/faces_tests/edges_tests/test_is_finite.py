from hypothesis import given

from tests.integration_tests.hints import BoundPortedEdgesPair
from tests.utils import equivalence
from . import strategies


@given(strategies.edges_pairs)
def test_basic(pair: BoundPortedEdgesPair) -> None:
    bound, ported = pair

    assert equivalence(bound.is_finite, ported.is_finite)
