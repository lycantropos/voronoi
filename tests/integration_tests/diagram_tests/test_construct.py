from hypothesis import given

from tests.integration_tests.hints import (BoundPortedDiagramsPair,
                                           BoundPortedPointsListsPair,
                                           BoundPortedSegmentsListsPair)
from tests.integration_tests.utils import are_bound_ported_diagrams_equal
from tests.utils import equivalence
from . import strategies


@given(strategies.empty_diagrams_pairs, strategies.multipoints)
def test_multipoints(pair: BoundPortedDiagramsPair,
                     multipoints_pair: BoundPortedPointsListsPair) -> None:
    bound_multipoint, ported_multipoint = multipoints_pair
    bound, ported = pair

    bound_result = bound.construct(bound_multipoint, [])
    ported_result = ported.construct(ported_multipoint, [])

    assert equivalence(bound_result, ported_result)
    assert are_bound_ported_diagrams_equal(bound, ported)


@given(strategies.empty_diagrams_pairs, strategies.multisegments)
def test_multisegments(pair: BoundPortedDiagramsPair,
                       multisegments_pair: BoundPortedSegmentsListsPair) -> None:
    bound_multisegment, ported_multisegment = multisegments_pair
    bound, ported = pair

    bound_result = bound.construct([], bound_multisegment)
    ported_result = ported.construct([], ported_multisegment)

    assert equivalence(bound_result, ported_result)
    assert are_bound_ported_diagrams_equal(bound, ported)
