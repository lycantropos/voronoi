from hypothesis import strategies

from tests.bind_tests.utils import (bound_geometry_categories,
                                    bound_source_categories)
from tests.port_tests.utils import (ported_geometry_categories,
                                    ported_source_categories)

geometry_categories_pairs = strategies.sampled_from(
        list(zip(bound_geometry_categories, ported_geometry_categories)))
source_categories_pairs = strategies.sampled_from(
        list(zip(bound_source_categories, ported_source_categories)))
