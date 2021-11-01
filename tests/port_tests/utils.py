from tests.port_tests.hints import (PortedGeometryCategory,
                                    PortedPoint,
                                    PortedPointsList,
                                    PortedSegment,
                                    PortedSegmentsList,
                                    PortedSourceCategory)
from tests.utils import (RawMultipoint,
                         RawMultisegment,
                         enum_to_values)

ported_geometry_categories = enum_to_values(PortedGeometryCategory)
ported_source_categories = enum_to_values(PortedSourceCategory)


def to_ported_multipoint(raw: RawMultipoint) -> PortedPointsList:
    result = []
    for point in raw.points:
        result.append(PortedPoint(point.x, point.y))
    return result


def to_ported_multisegment(raw: RawMultisegment) -> PortedSegmentsList:
    result = []
    for segment in raw.segments:
        result.append(
            PortedSegment(PortedPoint(segment.start.x, segment.start.y),
                          PortedPoint(segment.end.x, segment.end.y)))
    return result
