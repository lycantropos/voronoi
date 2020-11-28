from hypothesis import given

from tests.bind_tests.hints import BoundCell
from tests.integration_tests.hints import BoundPortedSourceCategoriesPair
from tests.integration_tests.utils import are_bound_ported_cells_equal
from tests.port_tests.hints import PortedCell
from . import strategies


@given(strategies.sizes, strategies.source_categories_pairs)
def test_basic(source_index: int,
               source_categories_pair: BoundPortedSourceCategoriesPair
               ) -> None:
    bound_source_category, ported_source_category = source_categories_pair

    bound, ported = (BoundCell(source_index, bound_source_category),
                     PortedCell(source_index, ported_source_category))

    assert are_bound_ported_cells_equal(bound, ported)
