from hypothesis import given

from tests.utils import (BoundPortedPointsPair,
                         equivalence)
from . import strategies


@given(strategies.points_pairs, strategies.points_pairs)
def test_basic(first_pair: BoundPortedPointsPair,
               second_pair: BoundPortedPointsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
