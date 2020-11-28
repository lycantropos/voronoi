from typing import List

from voronoi.beach_line_key import BeachLineKey as PortedBeachLineKey
from voronoi.beach_line_value import BeachLineValue as PortedBeachLineValue
from voronoi.big_float import BigFloat as PortedBigFloat
from voronoi.big_int import BigInt as PortedBigInt
from voronoi.builder import Builder as PortedBuilder
from voronoi.diagram import Diagram as PortedDiagram
from voronoi.enums import (GeometryCategory as PortedGeometryCategory,
                           SourceCategory as PortedSourceCategory)
from voronoi.events import (CircleEvent as PortedCircleEvent,
                            SiteEvent as PortedSiteEvent)
from voronoi.faces import (Cell as PortedCell,
                           Edge as PortedEdge,
                           Vertex as PortedVertex)
from voronoi.point import Point as PortedPoint
from voronoi.robust_difference import (RobustDifference
                                       as PortedRobustDifference)
from voronoi.robust_float import RobustFloat as PortedRobustFloat
from voronoi.segment import Segment as PortedSegment

PortedBeachLineKey = PortedBeachLineKey
PortedBeachLineValue = PortedBeachLineValue
PortedBigFloat = PortedBigFloat
PortedBigInt = PortedBigInt
PortedBuilder = PortedBuilder
PortedCell = PortedCell
PortedCircleEvent = PortedCircleEvent
PortedDiagram = PortedDiagram
PortedEdge = PortedEdge
PortedGeometryCategory = PortedGeometryCategory
PortedPoint = PortedPoint
PortedPointsList = List[PortedPoint]
PortedRobustDifference = PortedRobustDifference
PortedRobustFloat = PortedRobustFloat
PortedSegment = PortedSegment
PortedSegmentsList = List[PortedSegment]
PortedSiteEvent = PortedSiteEvent
PortedSourceCategory = PortedSourceCategory
PortedVertex = PortedVertex
