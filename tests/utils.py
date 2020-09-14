from enum import Enum
from typing import (List,
                    Tuple,
                    Type)

from _voronoi import (Point as BoundPoint,
                      Segment as BoundSegment,
                      SiteEvent as BoundSiteEvent,
                      SourceCategory as BoundSourceCategory)
from hypothesis.strategies import SearchStrategy

from voronoi.point import Point as PortedPoint
from voronoi.segment import Segment as PortedSegment
from voronoi.site_event import SiteEvent as PortedSiteEvent
from voronoi.source_category import SourceCategory as PortedSourceCategory

Strategy = SearchStrategy

BoundPoint = BoundPoint
BoundSegment = BoundSegment
BoundSiteEvent = BoundSiteEvent
BoundSourceCategory = BoundSourceCategory

PortedPoint = PortedPoint
PortedSegment = PortedSegment
PortedSiteEvent = PortedSiteEvent
PortedSourceCategory = PortedSourceCategory

BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSegmentsPair = Tuple[BoundSegment, PortedSegment]
BoundPortedSiteEventsPair = Tuple[BoundSiteEvent, PortedSiteEvent]
BoundPortedSourceCategoriesPair = Tuple[BoundSourceCategory,
                                        PortedSourceCategory]


def enum_to_values(cls: Type[Enum]) -> List[Enum]:
    return [value for _, value in sorted(cls.__members__.items())]


bound_source_categories = enum_to_values(BoundSourceCategory)
ported_source_categories = enum_to_values(PortedSourceCategory)


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def are_bound_ported_points_equal(bound: BoundPoint,
                                  ported: PortedPoint) -> bool:
    return bound.x == ported.x and bound.y == ported.y


def are_bound_ported_segments_equal(bound: BoundSegment,
                                    ported: PortedSegment) -> bool:
    return (are_bound_ported_points_equal(bound.start, ported.start)
            and are_bound_ported_points_equal(bound.end, ported.end))


def are_bound_ported_site_events_equal(bound: BoundSiteEvent,
                                       ported: PortedSiteEvent) -> bool:
    return (are_bound_ported_points_equal(bound.start, ported.start)
            and are_bound_ported_points_equal(bound.end, ported.end)
            and bound.sorted_index == ported.sorted_index
            and bound.initial_index == ported.initial_index
            and bound.is_inverse is ported.is_inverse
            and bound.source_category == ported.source_category)


def to_bound_with_ported_points_pair(x: int, y: int) -> BoundPortedPointsPair:
    return BoundPoint(x, y), PortedPoint(x, y)


def to_bound_with_ported_segments_pair(starts_pair: BoundPortedPointsPair,
                                       ends_pair: BoundPortedPointsPair
                                       ) -> BoundPortedSegmentsPair:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    return (BoundSegment(bound_start, bound_end),
            PortedSegment(ported_start, ported_end))


def to_bound_with_ported_site_events_pair(starts_pair: BoundPortedPointsPair,
                                          ends_pair: BoundPortedPointsPair,
                                          sorted_index: int,
                                          initial_index: int,
                                          is_inverse: bool,
                                          source_categories
                                          : BoundPortedSourceCategoriesPair
                                          ) -> BoundPortedSiteEventsPair:
    bound_start, ported_start = starts_pair
    bound_end, ported_end = ends_pair
    bound_source_category, ported_source_category = source_categories
    return (BoundSiteEvent(bound_start, bound_end, sorted_index, initial_index,
                           is_inverse, bound_source_category),
            PortedSiteEvent(ported_start, ported_end, sorted_index,
                            initial_index, is_inverse, ported_source_category))
