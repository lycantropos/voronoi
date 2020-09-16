from _voronoi import distance_to_segment_arc as bound
from hypothesis import given

from tests.utils import (BoundPortedPointsPair,
                         BoundPortedSiteEventsPair)
from voronoi.events import distance_to_segment_arc as ported
from . import strategies


@given(strategies.site_events_pairs, strategies.points_pairs)
def test_basic(events_pair: BoundPortedSiteEventsPair,
               points_pair: BoundPortedPointsPair) -> None:
    bound_event, ported_event = events_pair
    bound_point, ported_point = points_pair

    assert (bound(bound_event, bound_point)
            == ported(ported_event, ported_point))
