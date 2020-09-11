from typing import List

from hypothesis import given

from tests.utils import (BoundCell,
                         PortedCell,
                         are_bound_ported_cells_equal)
from . import strategies


@given(strategies.sizes, strategies.sizes, strategies.booleans,
       strategies.booleans, strategies.booleans, strategies.booleans,
       strategies.integers_64_lists, strategies.integers_64_lists,
       strategies.integers_32)
def test_basic(index: int,
               site: int,
               contains_point: bool,
               contains_segment: bool,
               is_open: bool,
               is_degenerate: bool,
               vertices_indices: List[int],
               edges_indices: List[int],
               source_category: int) -> None:
    bound, ported = (BoundCell(index, site, contains_point, contains_segment,
                               is_open, is_degenerate, vertices_indices,
                               edges_indices, source_category),
                     PortedCell(index, site, contains_point, contains_segment,
                                is_open, is_degenerate, vertices_indices,
                                edges_indices, source_category))

    assert are_bound_ported_cells_equal(bound, ported)
