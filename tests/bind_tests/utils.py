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


def to_bound_multipoint(raw: RawMultipoint) -> BoundPointsList:
    result = []
    for point in raw.points:
        result.append(BoundPoint(point.x, point.y))
    return result


def to_bound_multisegment(raw: RawMultisegment) -> BoundSegmentsList:
    result = []
    for segment in raw.segments:
        result.append(BoundSegment(
                BoundPoint(segment.start.x, segment.start.y),
                BoundPoint(segment.end.x, segment.end.y)))
    return result
