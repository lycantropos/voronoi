from hypothesis import strategies
from hypothesis_geometry import planar

from tests.port_tests.hints import (PortedCell,
                                    PortedDiagram,
                                    PortedEdge,
                                    PortedVertex)
from tests.port_tests.utils import (ported_source_categories,
                                    to_ported_multipoint,
                                    to_ported_multisegment)
from tests.strategies import (doubles,
                              integers_32,
                              sizes)
from tests.utils import to_maybe

booleans = strategies.booleans()
coordinates = doubles
empty_diagrams = strategies.builds(PortedDiagram)
source_categories = strategies.sampled_from(ported_source_categories)
cells = strategies.builds(PortedCell, sizes, source_categories)
vertices = strategies.builds(PortedVertex, coordinates, coordinates)
edges = strategies.builds(PortedEdge, to_maybe(vertices), cells,
                          booleans, booleans)
cells_lists = strategies.lists(cells)
edges_lists = strategies.lists(edges)
vertices_lists = strategies.lists(vertices)
diagrams = strategies.builds(PortedDiagram, cells_lists, edges_lists,
                             vertices_lists)
multipoints = planar.multipoints(integers_32).map(to_ported_multipoint)
multisegments = planar.multisegments(integers_32).map(to_ported_multisegment)
