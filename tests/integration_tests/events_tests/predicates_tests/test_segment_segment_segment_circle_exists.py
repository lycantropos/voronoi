from _voronoi import segment_segment_segment_circle_exists as bound
from hypothesis import given

from tests.integration_tests.hints import BoundPortedSiteEventsPair
from tests.utils import equivalence
from voronoi.events.predicates import (segment_segment_segment_circle_exists
                                       as ported)
from . import strategies


@given(strategies.site_events_pairs, strategies.site_events_pairs,
       strategies.site_events_pairs)
def test_basic(first_sites_pair: BoundPortedSiteEventsPair,
               second_sites_pair: BoundPortedSiteEventsPair,
               third_sites_pair: BoundPortedSiteEventsPair) -> None:
    bound_first_site, ported_first_site = first_sites_pair
    bound_second_site, ported_second_site = second_sites_pair
    bound_third_site, ported_third_site = third_sites_pair

    assert equivalence(bound(bound_first_site, bound_second_site,
                             bound_third_site),
                       ported(ported_first_site, ported_second_site,
                              ported_third_site))
