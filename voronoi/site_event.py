from reprit.base import generate_repr

from .point import Point
from .source_category import SourceCategory


class SiteEvent:
    __slots__ = ('start', 'end', 'sorted_index', 'initial_index', 'is_inverse',
                 'source_category')

    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end
        self.sorted_index = 0
        self.initial_index = 0
        self.is_inverse = False
        self.source_category = SourceCategory.SINGLE_POINT

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'SiteEvent') -> bool:
        return (self.start == other.start and self.end == other.end
                if isinstance(other, SiteEvent)
                else NotImplemented)

    def inverse(self) -> 'SiteEvent':
        self.start, self.end, self.is_inverse = (self.end, self.start,
                                                 not self.is_inverse)
        return self
