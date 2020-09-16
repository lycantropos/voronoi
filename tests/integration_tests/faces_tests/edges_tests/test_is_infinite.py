from hypothesis import given

from tests.utils import (BoundPortedEdgesPair,
                         equivalence)
from . import strategies


@given(strategies.edges_pairs)
def test_basic(pair: BoundPortedEdgesPair) -> None:
    bound, ported = pair

    assert equivalence(bound.is_infinite, ported.is_infinite)
