from typing import Tuple

from reprit.base import generate_repr

from .events import (SiteEvent,
                     horizontal_goes_through_right_arc_first)


class BeachLineKey:
    __slots__ = 'left_site', 'right_site'

    def __init__(self, left_site: SiteEvent, right_site: SiteEvent) -> None:
        self.left_site = left_site
        self.right_site = right_site

    __repr__ = generate_repr(__init__)

    def __lt__(self, other: 'BeachLineKey') -> bool:
        site, other_site = self.comparison_site, other.comparison_site
        point, other_point = site.comparison_point, other_site.comparison_point
        if point.x < other_point.x:
            # second node contains a new site
            return horizontal_goes_through_right_arc_first(
                    self.left_site, self.right_site, other_point)
        elif point.x > other_point.x:
            # first node contains a new site
            return not horizontal_goes_through_right_arc_first(
                    other.left_site, other.right_site, point)
        elif site.sorted_index == other_site.sorted_index:
            # both nodes are new
            # (inserted during same site event processing)
            return self.to_comparison_y() < other.to_comparison_y()
        elif site.sorted_index < other_site.sorted_index:
            y, flag = self.to_comparison_y(False)
            other_y, _ = other.to_comparison_y(True)
            return (not site.is_segment and flag < 0
                    if y == other_y
                    else y < other_y)
        else:
            y, _ = self.to_comparison_y(True)
            other_y, other_flag = other.to_comparison_y(False)
            return (other_site.is_segment or other_flag > 0
                    if y == other_y
                    else y < other_y)

    @property
    def comparison_site(self) -> SiteEvent:
        return (self.left_site
                if self.left_site.sorted_index > self.right_site.sorted_index
                else self.right_site)

    def to_comparison_y(self, is_new_node: bool = True) -> Tuple[int, int]:
        if self.left_site.sorted_index == self.right_site.sorted_index:
            return self.left_site.start.y, 0
        elif self.left_site.sorted_index > self.right_site.sorted_index:
            comparison_point = (self.left_site.start
                                if (not is_new_node
                                    and self.left_site.is_segment
                                    and self.left_site.is_vertical)
                                else self.left_site.end)
            return comparison_point.y, 1
        else:
            return self.right_site.start.y, -1
