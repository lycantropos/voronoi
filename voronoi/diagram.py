from typing import (List,
                    Optional,
                    Tuple)

from reprit.base import generate_repr

from .builder import Builder
from .events import (CircleEvent,
                     SiteEvent)
from .faces import (Cell,
                    Edge,
                    Vertex)
from .point import Point
from .segment import Segment


class Diagram:
    __slots__ = 'cells', 'edges', 'vertices'

    def __init__(self,
                 cells: Optional[List[Cell]] = None,
                 edges: Optional[List[Edge]] = None,
                 vertices: Optional[List[Vertex]] = None) -> None:
        self.cells = [] if cells is None else cells
        self.edges = [] if edges is None else edges
        self.vertices = [] if vertices is None else vertices

    __repr__ = generate_repr(__init__)

    @staticmethod
    def is_linear_edge(first_event: SiteEvent,
                       second_event: SiteEvent) -> bool:
        return (not Diagram.is_primary_edge(first_event, second_event)
                or first_event.is_segment is second_event.is_segment)

    @staticmethod
    def is_primary_edge(first_event: SiteEvent,
                        second_event: SiteEvent) -> bool:
        first_event_is_segment, second_event_is_segment = (
            first_event.is_segment, second_event.is_segment)
        if first_event_is_segment and not second_event_is_segment:
            return (first_event.start != second_event.start
                    and first_event.end != second_event.start)
        elif not first_event_is_segment and second_event_is_segment:
            return (second_event.start != first_event.start
                    and second_event.end != first_event.start)
        return True

    def clear(self) -> None:
        self.cells.clear()
        self.edges.clear()
        self.vertices.clear()

    def construct(self, points: List[Point], segments: List[Segment]) -> None:
        builder = Builder()
        for point in points:
            builder.insert_point(point)
        for segment in segments:
            builder.insert_segment(segment)
        builder.construct(self)

    def _build(self) -> None:
        self._remove_degenerate_edges()
        for edge in self.edges:
            edge.set_as_incident()
        self._remove_degenerate_vertices()
        # set up next/prev pointers for infinite edges
        if self.vertices:
            # update prev/next pointers for the ray edges
            self._update_ray_edges()
        elif self.edges:
            # update prev/next pointers for the line edges
            self._update_line_edges()

    def _insert_new_edge(self,
                         first_site: SiteEvent,
                         second_site: SiteEvent) -> Tuple[Edge, Edge]:
        # add the initial cell during the first edge insertion
        if not self.cells:
            self.cells.append(Cell(first_site.initial_index,
                                   first_site.source_category))
        # the second site represents a new site during site event processing,
        # add a new cell to the cell records
        self.cells.append(Cell(second_site.initial_index,
                               second_site.source_category))
        is_linear = self.is_linear_edge(first_site, second_site)
        is_primary = self.is_primary_edge(first_site, second_site)
        first_edge = Edge(None, self.cells[first_site.sorted_index], is_linear,
                          is_primary)
        second_edge = Edge(None, self.cells[second_site.sorted_index],
                           is_linear, is_primary)
        first_edge.twin, second_edge.twin = second_edge, first_edge
        self.edges.append(first_edge)
        self.edges.append(second_edge)
        return first_edge, second_edge

    def _insert_new_edge_from_intersection(self,
                                           first_site_event: SiteEvent,
                                           second_site_event: SiteEvent,
                                           circle_event: CircleEvent,
                                           first_bisector: Edge,
                                           second_bisector: Edge
                                           ) -> Tuple[Edge, Edge]:
        # add a new Voronoi vertex
        new_vertex = Vertex(circle_event.x, circle_event.y)
        self.vertices.append(new_vertex)
        # update vertex pointers of the old edges
        first_bisector.start = second_bisector.start = new_vertex
        is_linear = self.is_linear_edge(first_site_event, second_site_event)
        is_primary = self.is_primary_edge(first_site_event, second_site_event)
        first_edge = Edge(None, self.cells[first_site_event.sorted_index],
                          is_linear, is_primary)
        second_edge = Edge(new_vertex,
                           self.cells[second_site_event.sorted_index],
                           is_linear, is_primary)
        first_edge.next, second_edge.prev = (first_bisector,
                                             second_bisector.twin)
        first_edge.twin, second_edge.twin = second_edge, first_edge
        self.edges.append(first_edge)
        self.edges.append(second_edge)
        # update Voronoi prev/next pointers
        first_bisector.prev = first_edge
        first_bisector.twin.next = second_bisector
        second_bisector.prev = first_bisector.twin
        second_bisector.twin.next = second_edge
        return first_edge, second_edge

    def _process_single_site(self, site: SiteEvent) -> None:
        self.cells.append(Cell(site.initial_index, site.source_category))

    def _remove_degenerate_edges(self) -> None:
        first_degenerate_edge_index = 0
        for edge_index in range(0, len(self.edges), 2):
            edge = self.edges[edge_index]
            if edge.is_degenerate:
                edge.disconnect()
            else:
                if edge_index != first_degenerate_edge_index:
                    self.edges[first_degenerate_edge_index] = edge
                    next_edge = self.edges[first_degenerate_edge_index + 1] = (
                        self.edges[edge_index + 1])
                    edge.twin, next_edge.twin = next_edge, edge
                    if edge.prev is not None:
                        edge.prev.next, next_edge.next.prev = edge, next_edge
                    if next_edge.prev is not None:
                        edge.next.prev, next_edge.prev.next = edge, next_edge
                first_degenerate_edge_index += 2
        del self.edges[first_degenerate_edge_index:]

    def _remove_degenerate_vertices(self) -> None:
        first_degenerate_vertex_index = 0
        for index, vertex in enumerate(self.vertices):
            if vertex.is_degenerate:
                continue
            if index != first_degenerate_vertex_index:
                self.vertices[first_degenerate_vertex_index] = vertex
                cursor = vertex.incident_edge
                while True:
                    cursor.start = vertex
                    cursor = cursor.rot_next
                    if cursor is vertex.incident_edge:
                        break
            first_degenerate_vertex_index += 1
        del self.vertices[first_degenerate_vertex_index:]

    def _update_line_edges(self) -> None:
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

    def _update_ray_edges(self) -> None:
        for cell in self.cells:
            if cell.is_degenerate:
                continue
            # move to the previous edge in the clockwise direction
            # while it is possible
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
