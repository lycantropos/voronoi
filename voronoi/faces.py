from typing import Optional

from reprit.base import generate_repr

from .enums import (ComparisonResult,
                    GeometryCategory,
                    SourceCategory)
from .utils import compare_floats


class Cell:
    __slots__ = 'source_index', 'source_category', 'incident_edge'

    def __init__(self,
                 source_index: int,
                 source_category: SourceCategory) -> None:
        self.source_index = source_index
        self.source_category = source_category
        self.incident_edge = None  # type: Optional[Edge]

    __repr__ = generate_repr(__init__)

    @property
    def contains_point(self) -> bool:
        return self.source_category.belongs(GeometryCategory.POINT)

    @property
    def contains_segment(self) -> bool:
        return self.source_category.belongs(GeometryCategory.SEGMENT)

    @property
    def is_degenerate(self) -> bool:
        return self.incident_edge is None


class Vertex:
    __slots__ = 'x', 'y', 'incident_edge'

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.incident_edge = None  # type: Optional[Edge]

    __repr__ = generate_repr(__init__)

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
    __slots__ = ('start', 'cell', 'is_linear', 'is_primary', 'twin', 'prev',
                 'next')

    def __init__(self,
                 start: Optional[Vertex],
                 cell: Cell,
                 is_linear: bool,
                 is_primary: bool) -> None:
        self.start = start
        self.cell = cell
        self.is_linear = is_linear
        self.is_primary = is_primary
        self.twin = self.prev = self.next = None

    __repr__ = generate_repr(__init__)

    @property
    def end(self) -> Optional[Vertex]:
        return None if self.twin is None else self.twin.start

    @property
    def is_curved(self) -> bool:
        return not self.is_linear

    @property
    def is_degenerate(self) -> bool:
        return (self.start is not None
                and self.end is not None
                and self.start == self.end)

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

    def disconnect(self) -> None:
        vertex = self.start
        cursor = self.twin.rot_next
        while cursor is not self.twin:
            cursor.start = vertex
            cursor = cursor.rot_next
        twin = self.twin
        edge_rot_prev, edge_rot_next = self.rot_prev, self.rot_next
        twin_rot_prev, twin_rot_next = twin.rot_prev, twin.rot_next
        # update prev/next pointers for the incident edges
        edge_rot_next.twin.next = twin_rot_prev
        twin_rot_prev.prev = edge_rot_next.twin
        edge_rot_prev.prev = twin_rot_next.twin
        twin_rot_next.twin.next = edge_rot_prev

    def set_as_incident(self) -> None:
        self.cell.incident_edge = self
        if self.start is not None:
            self.start.incident_edge = self
