from hypothesis import given

from tests.utils import (BoundPortedGeometryCategoriesPair,
                         BoundPortedSourceCategoriesPair,
                         equivalence)
from . import strategies


@given(strategies.source_categories_pairs,
       strategies.geometry_categories_pairs)
def test_basic(pair: BoundPortedSourceCategoriesPair,
               geometry_categories: BoundPortedGeometryCategoriesPair) -> None:
    bound, ported = pair
    bound_geometry_category, ported_geometry_category = geometry_categories

    assert equivalence(bound.belongs(bound_geometry_category),
                       ported.belongs(ported_geometry_category))
