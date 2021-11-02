from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundBuilder
from tests.integration_tests.hints import BoundPortedSiteEventsListsPair
from tests.integration_tests.utils import are_bound_ported_builders_equal
from tests.port_tests.hints import PortedBuilder
from . import strategies


@given(strategies.indices_with_non_empty_site_events_lists_pairs)
def test_basic(index_with_site_events_lists_pair
               : Tuple[int, BoundPortedSiteEventsListsPair]) -> None:
    index, site_events_lists_pair = index_with_site_events_lists_pair
    bound_site_events, ported_site_events = site_events_lists_pair

    bound, ported = (BoundBuilder(index, bound_site_events),
                     PortedBuilder(index, ported_site_events))

    assert are_bound_ported_builders_equal(bound, ported)
