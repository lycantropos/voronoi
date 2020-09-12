from hypothesis import given

from tests.utils import (BoundEdge,
                         PortedEdge,
                         are_bound_ported_edges_equal)
from . import strategies


@given(strategies.integers_64, strategies.integers_64, strategies.booleans,
       strategies.booleans, strategies.integers_64, strategies.integers_64)
def test_basic(start_index: int,
               end_index: int,
               is_primary: bool,
               is_linear: bool,
               cell_index: int,
               twin_index: int) -> None:
    bound, ported = (BoundEdge(start_index, end_index, is_primary, is_linear,
                               cell_index, twin_index),
                     PortedEdge(start_index, end_index, is_primary, is_linear,
                                cell_index, twin_index))

    assert are_bound_ported_edges_equal(bound, ported)
