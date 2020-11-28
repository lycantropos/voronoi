from _voronoi import to_orientation as bound
from hypothesis import given

from tests.integration_tests.hints import BoundPortedPointsPair
from voronoi.utils import to_orientation as ported
from . import strategies


@given(strategies.points_pairs, strategies.points_pairs,
       strategies.points_pairs)
def test_basic(vertices: BoundPortedPointsPair,
               first_ray_points: BoundPortedPointsPair,
               second_ray_points: BoundPortedPointsPair) -> None:
    bound_vertex, ported_vertex = vertices
    bound_first_ray_point, ported_first_ray_point = first_ray_points
    bound_second_ray_point, ported_second_ray_point = second_ray_points

    assert (bound(bound_vertex, bound_first_ray_point, bound_second_ray_point)
            == ported(ported_vertex, ported_first_ray_point,
                      ported_second_ray_point))
