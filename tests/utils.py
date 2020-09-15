from enum import Enum
from typing import (List,
                    Tuple,
                    Type,
                    TypeVar,
                    Union)

from _voronoi import (Builder as BoundBuilder,
                      CircleEvent as BoundCircleEvent,
                      Point as BoundPoint,
                      Segment as BoundSegment,
                      SiteEvent as BoundSiteEvent,
                      SourceCategory as BoundSourceCategory)
from hypothesis.strategies import SearchStrategy

from voronoi.builder import Builder as PortedBuilder
from voronoi.enums import SourceCategory as PortedSourceCategory
from voronoi.events import (CircleEvent as PortedCircleEvent,
                            SiteEvent as PortedSiteEvent)
from voronoi.point import Point as PortedPoint
from voronoi.segment import Segment as PortedSegment

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy

BoundBuilder = BoundBuilder
BoundCircleEvent = BoundCircleEvent
BoundPoint = BoundPoint
BoundSegment = BoundSegment
BoundSiteEvent = BoundSiteEvent
BoundSourceCategory = BoundSourceCategory

PortedBuilder = PortedBuilder
PortedCircleEvent = PortedCircleEvent
PortedPoint = PortedPoint
PortedSegment = PortedSegment
PortedSiteEvent = PortedSiteEvent
PortedSourceCategory = PortedSourceCategory

BoundPortedBuildersPair = Tuple[BoundBuilder, PortedBuilder]
BoundPortedCircleEventsPair = Tuple[BoundCircleEvent, PortedCircleEvent]
BoundPortedPointsPair = Tuple[BoundPoint, PortedPoint]
BoundPortedSegmentsPair = Tuple[BoundSegment, PortedSegment]
BoundPortedSiteEventsPair = Tuple[BoundSiteEvent, PortedSiteEvent]
BoundPortedEventsPair = Union[BoundPortedCircleEventsPair,
                              BoundPortedSiteEventsPair]
BoundPortedSourceCategoriesPair = Tuple[BoundSourceCategory,
                                        PortedSourceCategory]


def enum_to_values(cls: Type[Enum]) -> List[Enum]:
    return [value for _, value in sorted(cls.__members__.items())]


bound_source_categories = enum_to_values(BoundSourceCategory)
ported_source_categories = enum_to_values(PortedSourceCategory)


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def transpose_pairs(pairs: List[Tuple[Domain, Range]]
                    ) -> Tuple[List[Domain], List[Range]]:
    return tuple(map(list, zip(*pairs))) if pairs else ([], [])


def are_bound_ported_builders_equal(bound: BoundBuilder,
                                    ported: PortedBuilder) -> bool:
    return (bound.index == ported.index
            and all(map(are_bound_ported_site_events_equal, bound.site_events,
                        ported.site_events)))


def are_bound_ported_circle_events_equal(bound: BoundCircleEvent,
                                         ported: PortedCircleEvent) -> bool:
    return (bound.center_x == ported.center_x
            and bound.center_y == ported.center_y
            and bound.lower_x == ported.lower_x
            and bound.is_active is ported.is_active)


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


def to_bound_with_ported_builders_pair(index: int,
                                       site_events_pair
                                       : List[BoundPortedSiteEventsPair]
                                       ) -> BoundPortedBuildersPair:
    bound_site_events, ported_site_events = site_events_pair
    return (BoundBuilder(index, bound_site_events),
            PortedBuilder(index, ported_site_events))


def to_bound_with_ported_circle_events_pair(center_x: int,
                                            center_y: int,
                                            lower_x: int,
                                            is_active: bool
                                            ) -> BoundPortedCircleEventsPair:
    return (BoundCircleEvent(center_x, center_y, lower_x, is_active),
            PortedCircleEvent(center_x, center_y, lower_x, is_active))


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
