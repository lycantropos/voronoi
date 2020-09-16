from typing import (List,
                    Optional)

from reprit.base import generate_repr

from .events import SiteEvent
from .faces import (Cell,
                    Edge,
                    Vertex)


class Diagram:
    __slots__ = 'cells', 'edges', 'vertices'

    def __init__(self,
                 cells: Optional[List[Cell]] = None,
                 edges: Optional[List[Edge]] = None,
                 vertices: Optional[List[Vertex]] = None):
        self.cells = [] if cells is None else cells
        self.edges = [] if edges is None else edges
        self.vertices = [] if vertices is None else vertices

    __repr__ = generate_repr(__init__)

    @staticmethod
    def is_primary(first_event: SiteEvent, second_event: SiteEvent) -> bool:
        first_event_is_segment, second_event_is_segment = (
            first_event.is_segment, second_event.is_segment)
        if first_event_is_segment and not second_event_is_segment:
            return (first_event.start != second_event.start
                    and first_event.end != second_event.start)
        elif not first_event_is_segment and second_event_is_segment:
            return (second_event.start != first_event.start
                    and second_event.end != first_event.start)
        return True

    @staticmethod
    def remove_edge(edge: Edge) -> None:
        vertex = edge.start
        cursor = edge.twin.rot_next
        while cursor is not edge.twin:
            cursor.start = vertex
            cursor = cursor.rot_next
        twin = edge.twin
        edge_rot_prev, edge_rot_next = edge.rot_prev, edge.rot_next
        twin_rot_prev, twin_rot_next = twin.rot_prev, twin.rot_next

        # update prev/next pointers for the incident edges
        edge_rot_next.twin.next = twin_rot_prev
        twin_rot_prev.prev = edge_rot_next.twin
        edge_rot_prev.prev = twin_rot_next.twin
        twin_rot_next.twin.next = edge_rot_prev
