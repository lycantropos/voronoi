from hypothesis import strategies
from hypothesis_geometry import planar

from tests.bind_tests.hints import (BoundCell,
                                    BoundDiagram,
                                    BoundEdge,
                                    BoundVertex)
from tests.bind_tests.utils import (bound_source_categories,
                                    to_bound_multipoint,
                                    to_bound_multisegment)
from tests.strategies import (doubles,
                              integers_32,
                              sizes)
from tests.utils import to_maybe

booleans = strategies.booleans()
coordinates = doubles
empty_diagrams = strategies.builds(BoundDiagram)
source_categories = strategies.sampled_from(bound_source_categories)
cells = strategies.builds(BoundCell, sizes,
                          source_categories)
vertices = strategies.builds(BoundVertex, coordinates, coordinates)
edges = strategies.builds(BoundEdge, to_maybe(vertices), cells,
                          booleans, booleans)
cells_lists = strategies.lists(cells)
edges_lists = strategies.lists(edges)
vertices_lists = strategies.lists(vertices)
diagrams = strategies.builds(BoundDiagram, cells_lists, edges_lists,
                             vertices_lists)
multipoints = planar.multipoints(integers_32).map(to_bound_multipoint)
multisegments = planar.multisegments(integers_32).map(to_bound_multisegment)
