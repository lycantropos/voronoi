from hypothesis import given

from tests.utils import (BoundPortedVerticesPair,
                         equivalence)
from . import strategies


@given(strategies.vertices_pairs)
def test_basic(pair: BoundPortedVerticesPair) -> None:
    bound, ported = pair

    assert equivalence(bound.is_degenerate, ported.is_degenerate)
