from hypothesis import given

from tests.utils import (BoundBuilder,
                         BoundPortedSiteEventsListsPair,
                         PortedBuilder,
                         are_bound_ported_builders_equal)
from . import strategies


@given(strategies.sizes, strategies.site_events_lists_pairs)
def test_basic(index: int,
               site_events_pair: BoundPortedSiteEventsListsPair) -> None:
    bound_site_events, ported_site_events = site_events_pair
    bound, ported = (BoundBuilder(index, bound_site_events),
                     PortedBuilder(index, ported_site_events))

    assert are_bound_ported_builders_equal(bound, ported)
