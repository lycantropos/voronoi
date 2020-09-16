from reprlib import recursive_repr
from typing import Optional

from reprit import seekers
from reprit.base import generate_repr

from .enums import (ComparisonResult,
                    GeometryCategory,
                    SourceCategory)
from .utils import compare_floats


class Vertex:
    __slots__ = 'x', 'y', 'incident_edge'

    def __init__(self,
                 x: float,
                 y: float,
                 incident_edge: Optional['Edge'] = None) -> None:
        self.x = x
        self.y = y
        self.incident_edge = incident_edge

    __repr__ = recursive_repr()(generate_repr(__init__))

    def __eq__(self, other: 'Vertex',
               *,
               ulps: int = 128) -> bool:
        return (compare_floats(self.x, other.x, ulps)
                is compare_floats(self.y, other.y, ulps)
                is ComparisonResult.EQUAL
                if isinstance(other, Vertex)
                else NotImplemented)

    @property
    def is_degenerate(self) -> bool:
        return self.incident_edge is None


class Edge:
    __slots__ = ('start', 'twin', 'next', 'prev', 'cell', 'is_linear',
                 'is_primary')

    def __init__(self,
                 start: Optional[Vertex],
                 twin: Optional['Edge'],
                 next_: Optional['Edge'],
                 prev: Optional['Edge'],
                 cell: Optional['Cell'],
                 is_linear: bool,
                 is_primary: bool) -> None:
        self.start = start
        self.twin = twin
        self.next = next_
        self.prev = prev
        self.cell = cell
        self.is_linear = is_linear
        self.is_primary = is_primary

    __repr__ = generate_repr(__init__,
                             field_seeker=seekers.complex_)

    @property
    def end(self) -> Optional[Vertex]:
        return None if self.twin is None else self.twin.start

    @property
    def is_curved(self) -> bool:
        return not self.is_linear

    @property
    def is_finite(self) -> bool:
        return not self.is_infinite

    @property
    def is_infinite(self) -> bool:
        return self.start is None or self.end is None

    @property
    def is_secondary(self) -> bool:
        return not self.is_primary

    @property
    def rot_next(self) -> Optional['Edge']:
        return None if self.prev is None else self.prev.twin

    @property
    def rot_prev(self) -> Optional['Edge']:
        return None if self.twin is None else self.twin.next


class Cell:
    __slots__ = 'source_index', 'source_category', 'incident_edge'

    def __init__(self,
                 source_index: int,
                 source_category: SourceCategory,
                 incident_edge: Optional[Edge] = None) -> None:
        self.source_index = source_index
        self.source_category = source_category
        self.incident_edge = incident_edge

    __repr__ = recursive_repr()(generate_repr(__init__))

    @property
    def contains_point(self) -> bool:
        return self.source_category.belongs(GeometryCategory.POINT)

    @property
    def contains_segment(self) -> bool:
        return self.source_category.belongs(GeometryCategory.SEGMENT)

    @property
    def is_degenerate(self) -> bool:
        return self.incident_edge is None
