from hypothesis import given

from tests.integration_tests.hints import BoundPortedSegmentsPair
from tests.utils import equivalence
from . import strategies


@given(strategies.segments_pairs, strategies.segments_pairs)
def test_basic(first_pair: BoundPortedSegmentsPair,
               second_pair: BoundPortedSegmentsPair) -> None:
    first_bound, first_ported = first_pair
    second_bound, second_ported = second_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
