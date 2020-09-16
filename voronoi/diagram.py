from typing import (List,
                    Optional)

from reprit.base import generate_repr

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
