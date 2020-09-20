from _voronoi import recompute_point_point_point_circle_event as bound
from hypothesis import given

from tests.utils import (BoundPortedCircleEventsPair,
                         BoundPortedSiteEventsPair,
                         are_bound_ported_circle_events_equal)
from voronoi.events.computers import (recompute_point_point_point_circle_event
                                      as ported)
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
    bound_first_site, ported_first_site = first_sites_pair
    bound_second_site, ported_second_site = second_sites_pair
    bound_third_site, ported_third_site = third_sites_pair

    bound(bound_circle_event, bound_first_site, bound_second_site,
          bound_third_site, recompute_center_x, recompute_center_y,
          recompute_lower_x)
    ported(ported_circle_event, ported_first_site, ported_second_site,
           ported_third_site, recompute_center_x, recompute_center_y,
           recompute_lower_x)

    assert are_bound_ported_circle_events_equal(bound_circle_event,
                                                ported_circle_event)
