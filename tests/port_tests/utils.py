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


def to_ported_multipoint(raw_multipoint: RawMultipoint) -> PortedPointsList:
    ported_multipoint = []
    for x, y in raw_multipoint:
        ported_multipoint.append(PortedPoint(x, y))
    return ported_multipoint


def to_ported_multisegment(raw_multisegment: RawMultisegment
                           ) -> PortedSegmentsList:
    ported_multisegment = []
    for (start_x, start_y), (end_x, end_y) in raw_multisegment:
        ported_multisegment.append(PortedSegment(PortedPoint(start_x, start_y),
                                                 PortedPoint(end_x, end_y)))
    return ported_multisegment
