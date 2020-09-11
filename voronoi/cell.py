from typing import List

from reprit.base import generate_repr


class Cell:
    __slots__ = ('index', 'site', 'contains_point', 'contains_segment',
                 'is_open', 'is_degenerate', 'vertices_indices',
                 'edges_indices', 'source_category')

    def __init__(self,
                 index: int,
                 site: int,
                 contains_point: bool,
                 contains_segment: bool,
                 is_open: bool,
                 is_degenerate: bool,
                 vertices_indices: List[int],
                 edges_indices: List[int],
                 source_category: int) -> None:
        self.index = index
        self.site = site
        self.contains_point = contains_point
        self.contains_segment = contains_segment
        self.is_open = is_open
        self.is_degenerate = is_degenerate
        self.vertices_indices = vertices_indices
        self.edges_indices = edges_indices
        self.source_category = source_category

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'Cell') -> bool:
        return (self.index == other.index
                and self.site == other.site
                and self.contains_point is other.contains_point
                and self.contains_segment is other.contains_segment
                and self.is_open is other.is_open
                and self.is_degenerate is other.is_degenerate
                and self.vertices_indices == other.vertices_indices
                and self.edges_indices == other.edges_indices
                and self.source_category == other.source_category
                if isinstance(other, Cell)
                else NotImplemented)
