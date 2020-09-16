from hypothesis import given

from tests.utils import (BoundPortedDiagramsPair,
                         are_bound_ported_diagrams_equal)
from . import strategies


@given(strategies.diagrams_pairs)
def test_basic(pair: BoundPortedDiagramsPair) -> None:
    bound, ported = pair

    assert are_bound_ported_diagrams_equal(bound, ported)
