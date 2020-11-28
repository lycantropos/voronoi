from hypothesis import given

from tests.integration_tests.hints import BoundPortedVerticesPair
from tests.utils import equivalence
from . import strategies


@given(strategies.vertices_pairs, strategies.vertices_pairs)
def test_basic(first_pair: BoundPortedVerticesPair,
               second_pair: BoundPortedVerticesPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
