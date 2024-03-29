import ctypes
from copy import copy
from operator import itemgetter
from typing import (TYPE_CHECKING,
                    List,
                    Optional,
                    Tuple)

from dendroid import red_black
from prioq.base import PriorityQueue
from reprit.base import generate_repr

from .beach_line_key import BeachLineKey
from .beach_line_value import BeachLineValue
from .enums import SourceCategory
from .events import (CircleEvent,
                     SiteEvent)
from .events.computers import compute_circle_event
from .point import (Point,
                    are_vertical_endpoints)
from .segment import Segment
from .utils import to_unique_just_seen

if TYPE_CHECKING:
    from .diagram import Diagram


class Builder:
    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        self._index = ctypes.c_size_t(value).value

    __slots__ = ('_index', '_beach_line', '_circle_events', '_end_points',
                 'site_events', '_site_event_index')

    def __init__(self,
                 index: int = 0,
                 site_events: Optional[List[SiteEvent]] = None) -> None:
        self.index = index
        self._beach_line = red_black.Tree.from_components([])
        self._circle_events = PriorityQueue(key=itemgetter(0))
        self._end_points = PriorityQueue(key=itemgetter(0))
        self.site_events = [] if site_events is None else site_events
        self._site_event_index = None

    __repr__ = generate_repr(__init__)

    @property
    def beach_line(self) -> List[Tuple[BeachLineKey, BeachLineValue]]:
        return [node.item for node in self._beach_line]

    @property
    def site_event(self) -> SiteEvent:
        return self.site_events[self._site_event_index]

    @property
    def site_event_index(self) -> int:
        return (len(self.site_events)
                if self._site_event_index is None
                else self._site_event_index)

    def activate_circle_event(self,
                              first_site: SiteEvent,
                              second_site: SiteEvent,
                              third_site: SiteEvent,
                              bisector_node: red_black.Node) -> None:
        event = CircleEvent(0., 0., 0.)
        # check if the three input sites create a circle event
        if compute_circle_event(event, first_site, second_site, third_site):
            # add the new circle event to the circle events queue;
            # update bisector's circle event iterator to point
            # to the new circle event in the circle event queue
            self._circle_events.push((event, bisector_node))
            bisector_node.value.circle_event = event

    def construct(self, output: 'Diagram') -> None:
        self.init_sites_queue()
        self.init_beach_line(output)
        while (self._circle_events
               or self._site_event_index < len(self.site_events)):
            if (not self._circle_events
                    or (self._site_event_index < len(self.site_events)
                        and self.site_event < self._circle_events.peek()[0])):
                self.process_site_event(output)
            else:
                self.process_circle_event(output)
            while (self._circle_events
                   and not self._circle_events.peek()[0].is_active):
                self._circle_events.pop()
        self._beach_line.clear()
        output._build()

    @staticmethod
    def deactivate_circle_event(value: BeachLineValue) -> None:
        if value.circle_event is not None:
            value.circle_event.deactivate()
            value.circle_event = None

    def init_beach_line(self, diagram: 'Diagram') -> None:
        if not self.site_events:
            return
        elif len(self.site_events) == 1:
            # handle single site event case
            diagram._process_single_site(self.site_events[0])
            self._site_event_index += 1
        else:
            skip = 0
            while (self._site_event_index < len(self.site_events)
                   and are_vertical_endpoints(self.site_event.start,
                                              self.site_events[0].start)
                   and self.site_event.is_vertical):
                self._site_event_index += 1
                skip += 1
            if skip == 1:
                # init beach line with the first two sites
                self.init_beach_line_default(diagram)
            else:
                # init beach line with collinear vertical sites
                self.init_beach_line_collinear_sites(diagram)

    def init_beach_line_collinear_sites(self, diagram: 'Diagram') -> None:
        first_index, second_index = 0, 1
        while second_index != self._site_event_index:
            # create a new beach line node
            first_site, second_site = (self.site_events[first_index],
                                       self.site_events[second_index])
            new_node = BeachLineKey(first_site, second_site)
            # update the diagram
            edge, _ = diagram._insert_new_edge(first_site, second_site)
            # insert a new bisector into the beach line
            self._beach_line.insert(new_node, BeachLineValue(edge))
            first_index += 1
            second_index += 1

    def init_beach_line_default(self, diagram: 'Diagram') -> None:
        # get the first and the second site event
        self.insert_new_arc(self.site_events[0], self.site_events[0],
                            self.site_events[1], diagram)
        # the second site was already processed, move the position
        self._site_event_index += 1

    def insert_new_arc(self,
                       first_arc_site: SiteEvent,
                       second_arc_site: SiteEvent,
                       site_event: SiteEvent,
                       output: 'Diagram') -> red_black.Node:
        # create two new bisectors with opposite directions
        new_left_node = BeachLineKey(first_arc_site, site_event)
        new_right_node = BeachLineKey(site_event, second_arc_site)
        # set correct orientation for the first site of the second node
        if site_event.is_segment:
            new_right_node.left_site.inverse()
        # update the output
        edges = output._insert_new_edge(second_arc_site, site_event)
        self._beach_line.insert(new_right_node, BeachLineValue(edges[1]))
        if site_event.is_segment:
            # update the beach line with temporary bisector,
            # that will # disappear after processing site event
            # corresponding to the second endpoint of the segment site
            new_node = BeachLineKey(site_event, site_event)
            new_node.right_site.inverse()
            node = self._beach_line.insert(new_node, BeachLineValue(None))
            # update the data structure that holds temporary bisectors
            self._end_points.push((site_event.end, node))
        return self._beach_line.insert(new_left_node, BeachLineValue(edges[0]))

    def init_sites_queue(self) -> None:
        self.site_events.sort()
        self.site_events = to_unique_just_seen(self.site_events)
        for index, event in enumerate(self.site_events):
            event.sorted_index = index
        self._site_event_index = 0

    def insert_point(self, point: Point) -> int:
        index = self.index
        self.site_events.append(SiteEvent.from_point(
                point,
                initial_index=index,
                source_category=SourceCategory.SINGLE_POINT))
        self.index += 1
        return index

    def insert_segment(self, segment: Segment) -> int:
        site_events = self.site_events
        index = self.index
        start, end = segment.start, segment.end
        site_events.append(SiteEvent.from_point(
                start,
                initial_index=index,
                source_category=SourceCategory.SEGMENT_START_POINT))
        site_events.append(SiteEvent.from_point(
                end,
                initial_index=index,
                source_category=SourceCategory.SEGMENT_END_POINT))
        site_events.append(
                SiteEvent(start, end,
                          source_category=SourceCategory.INITIAL_SEGMENT,
                          initial_index=index)
                if start < end
                else SiteEvent(end, start,
                               source_category=SourceCategory.REVERSE_SEGMENT,
                               initial_index=index))
        self.index += 1
        return index

    def process_circle_event(self, output: 'Diagram') -> None:
        circle_event, first_node = self._circle_events.pop()
        last_node = first_node
        second_site = copy(first_node.key.right_site)
        second_bisector = first_node.value.edge
        first_node = self._beach_line.predecessor(first_node)
        first_bisector = first_node.value.edge
        first_site = copy(first_node.key.left_site)
        if (not first_site.is_segment and second_site.is_segment
                and second_site.end == first_site.start):
            second_site.inverse()
        first_node.key.right_site = second_site
        first_node.value.edge, _ = output._insert_new_edge_from_intersection(
                first_site, second_site, circle_event, first_bisector,
                second_bisector)
        self._beach_line.remove(last_node)
        last_node = first_node
        if first_node is not self._beach_line.min():
            self.deactivate_circle_event(first_node.value)
            first_node = self._beach_line.predecessor(first_node)
            self.activate_circle_event(first_node.key.left_site, first_site,
                                       second_site, last_node)
        last_node = self._beach_line.successor(last_node)
        if last_node is not red_black.NIL:
            self.deactivate_circle_event(last_node.value)
            self.activate_circle_event(first_site, second_site,
                                       last_node.key.right_site, last_node)

    def process_site_event(self, output: 'Diagram') -> None:
        last_index = self._site_event_index + 1
        if not self.site_event.is_segment:
            while (self._end_points
                   and self._end_points.peek()[0] == self.site_event.start):
                _, node = self._end_points.pop()
                self._beach_line.remove(node)
        else:
            while (last_index < len(self.site_events)
                   and self.site_events[last_index].is_segment
                   and (self.site_events[last_index].start
                        == self.site_event.start)):
                last_index += 1
        # find the node in the binary search tree
        # with left arc lying above the new site point
        new_key = BeachLineKey(self.site_event, self.site_event)
        right_node = self._beach_line.supremum(new_key)
        while self._site_event_index < last_index:
            site_event = copy(self.site_event)
            left_node = right_node
            if right_node is red_black.NIL:
                # the above arc corresponds to the second arc of the last node,
                # move the iterator to the last node
                left_node = self._beach_line.max()
                # get the second site of the last node
                arc_site = left_node.key.right_site
                # insert new nodes into the beach line, update the output
                right_node = self.insert_new_arc(arc_site, arc_site,
                                                 site_event, output)
                # add a candidate circle to the circle event queue;
                # there could be only one new circle event
                # formed by a new bisector and the one on the left
                self.activate_circle_event(left_node.key.left_site,
                                           left_node.key.right_site,
                                           site_event, right_node)
            elif right_node is self._beach_line.min():
                # the above arc corresponds to the first site of the first node
                arc_site = right_node.key.left_site
                # Insert new nodes into the beach line. Update the output.
                left_node = self.insert_new_arc(arc_site, arc_site, site_event,
                                                output)
                # if the site event is a segment, update its direction
                if site_event.is_segment:
                    site_event.inverse()
                # add a candidate circle to the circle event queue;
                # there could be only one new circle event
                # formed by a new bisector and the one on the right
                self.activate_circle_event(site_event,
                                           right_node.key.left_site,
                                           right_node.key.right_site,
                                           right_node)
                right_node = left_node
            else:
                # the above arc corresponds neither to the first,
                # nor to the last site in the beach line
                second_arc_site = right_node.key.left_site
                third_site = right_node.key.right_site
                # remove the candidate circle from the event queue
                self.deactivate_circle_event(right_node.value)
                left_node = self._beach_line.predecessor(left_node)
                first_arc_site = left_node.key.right_site
                first_site = left_node.key.left_site
                # insert new nodes into the beach line. Update the output
                new_node = self.insert_new_arc(first_arc_site, second_arc_site,
                                               site_event, output)
                # add candidate circles to the circle event queue;
                # there could be up to two circle events
                # formed by a new bisector and the one on the left or right
                self.activate_circle_event(first_site, first_arc_site,
                                           site_event, new_node)
                # if the site event is a segment, update its direction
                if site_event.is_segment:
                    site_event.inverse()
                self.activate_circle_event(site_event, second_arc_site,
                                           third_site, right_node)
                right_node = new_node
            self._site_event_index += 1
