from _voronoi import recompute_segment_segment_segment_circle_event as bound
from hypothesis import given

from tests.integration_tests.hints import (BoundPortedCircleEventsPair,
                                           BoundPortedSiteEventsPair)
from tests.integration_tests.utils import are_bound_ported_circle_events_equal
from voronoi.events.computers import (
    recompute_segment_segment_segment_circle_event as ported)
from . import strategies


@given(strategies.circle_events_pairs, strategies.site_events_pairs,
       strategies.site_events_pairs, strategies.site_events_pairs,
       strategies.booleans, strategies.booleans, strategies.booleans)
def test_basic(circle_events_pair: BoundPortedCircleEventsPair,
               first_sites_pair: BoundPortedSiteEventsPair,
               second_sites_pair: BoundPortedSiteEventsPair,
               third_sites_pair: BoundPortedSiteEventsPair,
               recompute_center_x: bool,
               recompute_center_y: bool,
               recompute_lower_x: bool) -> None:
    bound_circle_event, ported_circle_event = circle_events_pair
    first_site_bound, first_site_ported = first_sites_pair
    second_site_bound, second_site_ported = second_sites_pair
    third_site_bound, third_site_ported = third_sites_pair

    bound(bound_circle_event, first_site_bound, second_site_bound,
          third_site_bound, recompute_center_x, recompute_center_y,
          recompute_lower_x)
    ported(ported_circle_event, first_site_ported, second_site_ported,
           third_site_ported, recompute_center_x, recompute_center_y,
           recompute_lower_x)

    assert are_bound_ported_circle_events_equal(bound_circle_event,
                                                ported_circle_event)
