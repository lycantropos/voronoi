from hypothesis import given

from tests.integration_tests.hints import (BoundPortedBuildersPair,
                                           BoundPortedPointsPair)
from tests.integration_tests.utils import are_bound_ported_builders_equal
from . import strategies


@given(strategies.builders_pairs, strategies.points_pairs)
def test_basic(pair: BoundPortedBuildersPair,
               points_pair: BoundPortedPointsPair) -> None:
    bound, ported = pair
    bound_point, ported_point = points_pair

    bound_result = bound.insert_point(bound_point)
    ported_result = ported.insert_point(ported_point)

    assert bound_result == ported_result
    assert are_bound_ported_builders_equal(bound, ported)
