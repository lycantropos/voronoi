from hypothesis import given

from tests.bind_tests.hints import BoundBeachLineKey
from tests.integration_tests.hints import BoundPortedSiteEventsPair
from tests.integration_tests.utils import (
    are_bound_ported_beach_line_keys_equal)
from tests.port_tests.hints import PortedBeachLineKey
from . import strategies


@given(strategies.site_events_pairs, strategies.site_events_pairs)
def test_basic(left_sites_pair: BoundPortedSiteEventsPair,
               right_sites_pair: BoundPortedSiteEventsPair) -> None:
    bound_left_site, ported_left_site = left_sites_pair
    bound_right_site, ported_right_site = right_sites_pair
    bound, ported = (BoundBeachLineKey(bound_left_site, bound_right_site),
                     PortedBeachLineKey(ported_left_site, ported_right_site))

    assert are_bound_ported_beach_line_keys_equal(bound, ported)
