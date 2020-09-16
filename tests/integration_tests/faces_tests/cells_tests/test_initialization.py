from hypothesis import given

from tests.utils import (BoundCell,
                         BoundPortedMaybeEdgesPair,
                         BoundPortedSourceCategoriesPair,
                         PortedCell,
                         are_bound_ported_cells_equal)
from . import strategies


@given(strategies.sizes, strategies.source_categories_pairs,
       strategies.maybe_edges_pairs)
def test_basic(source_index: int,
               source_categories_pair: BoundPortedSourceCategoriesPair,
               incident_edges_pair: BoundPortedMaybeEdgesPair) -> None:
    bound_source_category, ported_source_category = source_categories_pair
    bound_incident_edge, ported_incident_edge = incident_edges_pair
    bound, ported = (BoundCell(source_index, bound_source_category,
                               bound_incident_edge),
                     PortedCell(source_index, ported_source_category,
                                ported_incident_edge))

    assert are_bound_ported_cells_equal(bound, ported)
