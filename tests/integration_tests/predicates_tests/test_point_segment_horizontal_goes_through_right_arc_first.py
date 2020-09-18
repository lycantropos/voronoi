from _voronoi import (point_segment_horizontal_goes_through_right_arc_first
                      as bound)
from hypothesis import given

from tests.utils import (BoundPortedPointsPair,
                         BoundPortedSiteEventsPair,
                         equivalence)
from voronoi.predicates import \
    point_segment_horizontal_goes_through_right_arc_first as ported
from . import strategies


@given(strategies.site_events_pairs, strategies.site_events_pairs,
       strategies.points_pairs, strategies.booleans)
def test_basic(left_sites_pair: BoundPortedSiteEventsPair,
               right_sites_pair: BoundPortedSiteEventsPair,
               points_pair: BoundPortedPointsPair,
               reverse_order: bool) -> None:
    bound_left_site, ported_left_site = left_sites_pair
    bound_right_site, ported_right_site = right_sites_pair
    bound_point, ported_point = points_pair

    assert equivalence(bound(bound_left_site, bound_right_site, bound_point,
                             reverse_order),
                       ported(ported_left_site, ported_right_site,
                              ported_point, reverse_order))
