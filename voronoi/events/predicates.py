from voronoi.enums import Orientation
from voronoi.events.models import SiteEvent
from voronoi.utils import to_orientation


def point_point_point_circle_exists(first_site: SiteEvent,
                                    second_site: SiteEvent,
                                    third_site: SiteEvent) -> bool:
    return to_orientation(first_site.start, second_site.start,
                          third_site.start) is Orientation.RIGHT


def point_point_segment_circle_exists(first_site: SiteEvent,
                                      second_site: SiteEvent,
                                      third_site: SiteEvent,
                                      segment_index: int) -> bool:
    if segment_index == 2:
        return (third_site.start != first_site.start
                or third_site.end != second_site.start)
    else:
        first_orientation = to_orientation(first_site.start, second_site.start,
                                           third_site.start)
        second_orientation = to_orientation(first_site.start,
                                            second_site.start,
                                            third_site.end)
        if segment_index == 1 and first_site.start.x >= second_site.start.x:
            return first_orientation is Orientation.RIGHT
        elif segment_index == 3 and second_site.start.x >= first_site.start.x:
            return second_orientation is Orientation.RIGHT
        else:
            return (first_orientation is Orientation.RIGHT
                    or second_orientation is Orientation.RIGHT)


def point_segment_segment_circle_exists(first_site: SiteEvent,
                                        second_site: SiteEvent,
                                        third_site: SiteEvent,
                                        point_index: int) -> bool:
    return (second_site.sorted_index != third_site.sorted_index
            and (point_index != 2
                 or (second_site.is_inverse or not third_site.is_inverse)
                 and (second_site.is_inverse is not third_site.is_inverse
                      or to_orientation(second_site.start, first_site.start,
                                        third_site.end)
                      is Orientation.RIGHT)))


def segment_segment_segment_circle_exists(first_site: SiteEvent,
                                          second_site: SiteEvent,
                                          third_site: SiteEvent) -> bool:
    return (first_site.sorted_index != second_site.sorted_index
            != third_site.sorted_index)
