from hypothesis import given

from tests.integration_tests.hints import (BoundPortedCircleEventsPair,
                                           BoundPortedSiteEventsPair)
from tests.utils import equivalence
from . import strategies


@given(strategies.circle_events_pairs, strategies.site_events_pairs)
def test_basic(first_pair: BoundPortedCircleEventsPair,
               sites_pair: BoundPortedSiteEventsPair) -> None:
    bound, ported = first_pair
    bound_site, ported_site = sites_pair

    assert equivalence(bound.lies_outside_vertical_segment(bound_site),
                       ported.lies_outside_vertical_segment(ported_site))
