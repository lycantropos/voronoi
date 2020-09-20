from hypothesis import given

from tests.utils import (BoundPortedSiteEventsPair,
                         are_bound_ported_points_equal)
from . import strategies


@given(strategies.site_events_pairs)
def test_basic(pair: BoundPortedSiteEventsPair) -> None:
    bound, ported = pair

    assert are_bound_ported_points_equal(bound.comparison_point,
                                         ported.comparison_point)
