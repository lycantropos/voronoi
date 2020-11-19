from typing import Tuple

from hypothesis import given

from tests.utils import (BoundPortedDiagramsPair,
                         BoundPortedPointsListsPair,
                         BoundPortedSegmentsListsPair,
                         are_bound_ported_diagrams_equal,
                         equivalence)
from . import strategies


@given(strategies.empty_diagrams_pairs,
       strategies.multipoints_with_multisegments_pairs)
def test_basic(pair: BoundPortedDiagramsPair,
               multipoints_with_multisegments_pair
               : Tuple[BoundPortedPointsListsPair,
                       BoundPortedSegmentsListsPair]) -> None:
    multipoints_pair, multisegments_pair = multipoints_with_multisegments_pair
    bound_multipoint, ported_multipoint = multipoints_pair
    bound_multisegment, ported_multisegment = multisegments_pair
    bound, ported = pair

    bound_result = bound.construct(bound_multipoint, bound_multisegment)
    ported_result = ported.construct(ported_multipoint, ported_multisegment)

    assert equivalence(bound_result, ported_result)
    assert are_bound_ported_diagrams_equal(bound, ported)
