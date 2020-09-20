from _voronoi import to_segment_segment_segment_circle_event as bound
from hypothesis import given

from tests.utils import (BoundPortedSiteEventsPair,
                         are_bound_ported_circle_events_equal)
from voronoi.events import to_segment_segment_segment_circle_event as ported
from . import strategies


@given(strategies.site_events_pairs, strategies.site_events_pairs,
       strategies.site_events_pairs, strategies.booleans, strategies.booleans,
       strategies.booleans)
def test_basic(first_sites_pair: BoundPortedSiteEventsPair,
               second_sites_pair: BoundPortedSiteEventsPair,
               third_sites_pair: BoundPortedSiteEventsPair,
               recompute_center_x: bool,
               recompute_center_y: bool,
               recompute_lower_x: bool) -> None:
    first_site_bound, first_site_ported = first_sites_pair
    second_site_bound, second_site_ported = second_sites_pair
    third_site_bound, third_site_ported = third_sites_pair

    bound_result = bound(first_site_bound, second_site_bound, third_site_bound,
                         recompute_center_x, recompute_center_y,
                         recompute_lower_x)
    ported_result = ported(first_site_ported, second_site_ported,
                           third_site_ported, recompute_center_x,
                           recompute_center_y, recompute_lower_x)

    assert are_bound_ported_circle_events_equal(bound_result, ported_result)
