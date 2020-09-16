from hypothesis import strategies

from tests.utils import (bound_geometry_categories,
                         bound_source_categories,
                         ported_geometry_categories,
                         ported_source_categories)

geometry_categories_pairs = strategies.sampled_from(
        list(zip(bound_geometry_categories, ported_geometry_categories)))
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
