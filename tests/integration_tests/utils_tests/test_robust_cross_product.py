from _voronoi import robust_cross_product as bound
from hypothesis import given

from voronoi.utils import robust_cross_product as ported
from . import strategies


@given(strategies.coordinates, strategies.coordinates, strategies.coordinates,
       strategies.coordinates)
def test_basic(first_dx: int,
               first_dy: int,
               second_dx: int,
               second_dy: int) -> None:
    assert (bound(first_dx, first_dy, second_dx, second_dy)
            == ported(first_dx, first_dy, second_dx, second_dy))
