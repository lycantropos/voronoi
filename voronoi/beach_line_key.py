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
