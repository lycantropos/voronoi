from hypothesis import given

from tests.integration_tests.hints import BoundPortedCircleEventsPair
from tests.utils import equivalence
from . import strategies


@given(strategies.circle_events_pairs, strategies.circle_events_pairs)
def test_basic(first_pair: BoundPortedCircleEventsPair,
               second_pair: BoundPortedCircleEventsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
