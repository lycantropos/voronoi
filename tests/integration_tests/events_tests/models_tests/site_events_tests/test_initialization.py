from hypothesis import given

from tests.bind_tests.hints import BoundSiteEvent
from tests.integration_tests.hints import (BoundPortedPointsPair,
                                           BoundPortedSourceCategoriesPair)
from tests.integration_tests.utils import are_bound_ported_site_events_equal
from tests.port_tests.hints import PortedSiteEvent
from . import strategies


@given(strategies.points_pairs, strategies.points_pairs, strategies.sizes,
       strategies.sizes, strategies.booleans,
       strategies.source_categories_pairs)
def test_basic(starts_pair: BoundPortedPointsPair,
               ends_pair: BoundPortedPointsPair,
               sorted_index: int,
               initial_index: int,
               is_inverse: bool,
               source_categories: BoundPortedSourceCategoriesPair) -> None:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    bound_source_category, ported_source_category = source_categories
    bound, ported = (BoundSiteEvent(bound_start, bound_end, sorted_index,
                                    initial_index, is_inverse,
                                    bound_source_category),
                     PortedSiteEvent(ported_start, ported_end, sorted_index,
                                     initial_index, is_inverse,
                                     ported_source_category))

    assert are_bound_ported_site_events_equal(bound, ported)
