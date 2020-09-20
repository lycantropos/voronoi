from _voronoi import robust_cross_product as bound
from hypothesis import given

from voronoi.utils import robust_cross_product as ported
from . import strategies


@given(strategies.integers_64, strategies.integers_64, strategies.integers_64,
       strategies.integers_64)
def test_basic(first_dx: int,
               first_dy: int,
               second_dx: int,
               second_dy: int) -> None:
    bound_result = bound(first_dx, first_dy, second_dx, second_dy)
    ported_result = ported(first_dx, first_dy, second_dx, second_dy)

    assert bound_result == ported_result
