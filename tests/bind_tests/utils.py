from tests.bind_tests.hints import (BoundGeometryCategory,
                                    BoundPoint,
                                    BoundPointsList,
                                    BoundSegment,
                                    BoundSegmentsList,
                                    BoundSourceCategory)
from tests.utils import (RawMultipoint,
                         RawMultisegment,
                         enum_to_values)

bound_geometry_categories = enum_to_values(BoundGeometryCategory)
bound_source_categories = enum_to_values(BoundSourceCategory)


def to_bound_multipoint(raw_multipoint: RawMultipoint) -> BoundPointsList:
    bound_multipoint = []
    for x, y in raw_multipoint:
        bound_multipoint.append(BoundPoint(x, y))
    return bound_multipoint


def to_bound_multisegment(raw_multisegment: RawMultisegment
                          ) -> BoundSegmentsList:
    bound_multisegment = []
    for (start_x, start_y), (end_x, end_y) in raw_multisegment:
        bound_multisegment.append(BoundSegment(BoundPoint(start_x, start_y),
                                               BoundPoint(end_x, end_y)))
    return bound_multisegment
