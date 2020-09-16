from hypothesis import given

from tests.utils import (BoundPortedCellsPair,
                         equivalence)
from . import strategies


@given(strategies.cells_pairs)
def test_basic(pair: BoundPortedCellsPair) -> None:
    bound, ported = pair

    assert equivalence(bound.contains_point, ported.contains_point)
