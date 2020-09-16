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

    def clear(self) -> None:
        self.cells.clear()
        self.edges.clear()
        self.vertices.clear()

    def _build(self) -> None:
        last_edge_index = 0
        for index, edge in enumerate(self.edges):
            start, end = edge.start, edge._end
            if start is not None and end is not None and start == end:
                self.remove_edge(edge)
            else:
                if index != last_edge_index:
                    self.edges[last_edge_index] = edge
                    next_edge = self.edges[last_edge_index + 1] = (
                        self.edges[index + 1])
                    edge.twin, next_edge.twin = next_edge, edge
                    if edge.prev is not None:
                        edge.prev.next, next_edge.next.prev = edge, next_edge
                    if next_edge.prev is not None:
                        edge.next.prev, next_edge.prev.next = edge, next_edge
                last_edge_index += 2
        del self.edges[last_edge_index:]
        # set up incident edge pointers for cells and vertices
        for edge in self.edges:
            edge.cell.incident_edge = edge
            if edge.start is not None:
                edge.start.incident_edge = edge
        # remove degenerate vertices
        last_vertex_index = 0
        for index, vertex in enumerate(self.vertices):
            if vertex.incident_edge is not None:
                if index != last_vertex_index:
                    self.vertices[last_vertex_index] = vertex
                    cursor = vertex.incident_edge
                    while True:
                        cursor.start = vertex
                        cursor = cursor.rot_next
                        if cursor is vertex.incident_edge:
                            break
                last_vertex_index += 1
        del self.vertices[last_vertex_index:]
        # set up next/prev pointers for infinite edges
        if not self.vertices:
            if self.edges:
                # update prev/next pointers for the line edges
                edge_index = 0
                edge = self.edges[edge_index]
                edge.prev = edge.next = edge
                edge_index += 1
                edge = self.edges[edge_index]
                edge_index += 1
                while edge_index < len(self.edges):
                    next_edge = self.edges[edge_index]
                    edge_index += 1
                    edge.prev = edge.next = next_edge
                    next_edge.prev = next_edge.next = edge
                    edge = self.edges[edge_index]
                    edge_index += 1
                edge.prev = edge.next = edge
        else:
            # update prev/next pointers for the ray edges
            for cell in self.cells:
                if cell.is_degenerate:
                    continue
                # move to the previous edge while it is possible
                # in the clockwise direction
                left_edge = cell.incident_edge
                while left_edge.prev is not None:
                    left_edge = left_edge.prev
                    # terminate if this is not a boundary cell
                    if left_edge is cell.incident_edge:
                        break
                if left_edge.prev is not None:
                    continue
                right_edge = cell.incident_edge
                while right_edge.next is not None:
                    right_edge = right_edge.next
                left_edge.prev, right_edge.next = right_edge, left_edge

    def _process_single_site(self, site: SiteEvent) -> None:
        self.cells.append(Cell(site.initial_index, site.source_category))
