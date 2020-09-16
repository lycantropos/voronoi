from hypothesis import given

from tests.utils import (BoundPortedCellsPair,
                         equivalence)
from . import strategies


@given(strategies.cells_pairs, strategies.cells_pairs)
def test_basic(first_pair: BoundPortedCellsPair,
               second_pair: BoundPortedCellsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
