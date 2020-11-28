from hypothesis import given

from tests.integration_tests.hints import (BoundPortedBuildersPair,
                                           BoundPortedSegmentsPair)
from tests.integration_tests.utils import are_bound_ported_builders_equal
from . import strategies


@given(strategies.builders_pairs, strategies.segments_pairs)
def test_basic(pair: BoundPortedBuildersPair,
               segments_pair: BoundPortedSegmentsPair) -> None:
    bound, ported = pair
    bound_segment, ported_segment = segments_pair

    bound_result = bound.insert_segment(bound_segment)
    ported_result = ported.insert_segment(ported_segment)

    assert bound_result == ported_result
    assert are_bound_ported_builders_equal(bound, ported)
