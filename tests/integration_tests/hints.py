from typing import (List,
                    Optional,
                    Tuple,
                    Union)

from tests.bind_tests.hints import (BoundBeachLineKey,
                                    BoundBigFloat,
                                    BoundBigInt,
                                    BoundBuilder,
                                    BoundCell,
                                    BoundCircleEvent,
                                    BoundDiagram,
                                    BoundEdge,
                                    BoundGeometryCategory,
                                    BoundPoint,
                                    BoundRobustDifference,
                                    BoundRobustFloat,
                                    BoundSegment,
                                    BoundSiteEvent,
                                    BoundSourceCategory,
                                    BoundVertex)
from tests.port_tests.hints import (PortedBeachLineKey,
                                    PortedBigFloat,
                                    PortedBigInt,
                                    PortedBuilder,
                                    PortedCell,
                                    PortedCircleEvent,
                                    PortedDiagram,
                                    PortedEdge,
                                    PortedGeometryCategory,
                                    PortedPoint,
                                    PortedRobustDifference,
                                    PortedRobustFloat,
                                    PortedSegment,
                                    PortedSiteEvent,
                                    PortedSourceCategory,
                                    PortedVertex)

BoundPortedBeachLineKeysPair = Tuple[BoundBeachLineKey, PortedBeachLineKey]
BoundPortedBigFloatsPair = Tuple[BoundBigFloat, PortedBigFloat]
BoundPortedBigIntsPair = Tuple[BoundBigInt, PortedBigInt]
BoundPortedBigIntsPairsPair = Tuple[Tuple[BoundBigInt, BoundBigInt],
                                    Tuple[PortedBigInt, PortedBigInt]]
BoundPortedBigIntsQuadrupletsPair = Tuple[Tuple[BoundBigInt, BoundBigInt,
                                                BoundBigInt, BoundBigInt],
                                          Tuple[PortedBigInt, PortedBigInt,
                                                PortedBigInt, PortedBigInt]]
BoundPortedBigIntsTripletsPair = Tuple[Tuple[BoundBigInt, BoundBigInt,
                                             BoundBigInt],
                                       Tuple[PortedBigInt, PortedBigInt,
                                             PortedBigInt]]
BoundPortedBuildersPair = Tuple[BoundBuilder, PortedBuilder]
BoundPortedBuildersWithDiagramsPair = Tuple[
    Tuple[BoundBuilder, BoundDiagram], Tuple[PortedBuilder, PortedDiagram]]
BoundPortedCellsPair = Tuple[BoundCell, PortedCell]
BoundPortedCellsListsPair = Tuple[List[BoundCell], List[PortedCell]]
BoundPortedCircleEventsPair = Tuple[BoundCircleEvent, PortedCircleEvent]
BoundPortedMaybeCircleEventsPair = Tuple[Optional[BoundCircleEvent],
                                         Optional[PortedCircleEvent]]
BoundPortedDiagramsPair = Tuple[BoundDiagram, PortedDiagram]
BoundPortedEdgesPair = Tuple[BoundEdge, PortedEdge]
BoundPortedEdgesListsPair = Tuple[List[BoundEdge], List[PortedEdge]]
BoundPortedMaybeEdgesPair = Tuple[Optional[BoundEdge], Optional[PortedEdge]]
BoundPortedGeometryCategoriesPair = Tuple[BoundGeometryCategory,
                                          PortedGeometryCategory]
BoundPortedPointsListsPair = Tuple[List[BoundPoint], List[PortedPoint]]
BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedRobustDifferencesPair = Tuple[BoundRobustDifference,
                                         PortedRobustDifference]
BoundPortedRobustFloatsPair = Tuple[BoundRobustFloat, PortedRobustFloat]
BoundPortedRobustDifferencesOrFloatsPair = Union[
    BoundPortedRobustDifferencesPair, BoundPortedRobustFloatsPair]
BoundPortedSegmentsListsPair = Tuple[List[BoundSegment], List[PortedSegment]]
BoundPortedSegmentsPair = Tuple[BoundSegment, PortedSegment]
BoundPortedSiteEventsPair = Tuple[BoundSiteEvent, PortedSiteEvent]
BoundPortedSiteEventsListsPair = Tuple[List[BoundSiteEvent],
                                       List[PortedSiteEvent]]
BoundPortedEventsPair = Union[BoundPortedCircleEventsPair,
                              BoundPortedSiteEventsPair]
BoundPortedSourceCategoriesPair = Tuple[BoundSourceCategory,
                                        PortedSourceCategory]
BoundPortedVerticesPair = Tuple[BoundVertex, PortedVertex]
BoundPortedVerticesListsPair = Tuple[List[BoundVertex], List[PortedVertex]]
BoundPortedMaybeVerticesPair = Tuple[Optional[BoundVertex],
                                     Optional[PortedVertex]]
