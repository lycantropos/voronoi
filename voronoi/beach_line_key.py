from typing import Tuple

from reprit.base import generate_repr

from .events import SiteEvent


class BeachLineKey:
    __slots__ = 'left_site', 'right_site'

    def __init__(self, left_site: SiteEvent, right_site: SiteEvent) -> None:
        self.left_site = left_site
        self.right_site = right_site

    __repr__ = generate_repr(__init__)

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
