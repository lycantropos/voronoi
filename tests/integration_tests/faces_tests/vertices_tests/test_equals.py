from hypothesis import given

from tests.utils import (BoundPortedVerticesPair,
                         equivalence)
from . import strategies


@given(strategies.vertices_pairs, strategies.vertices_pairs)
def test_basic(first_pair: BoundPortedVerticesPair,
               second_pair: BoundPortedVerticesPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
