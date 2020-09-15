#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <sstream>
#include <stdexcept>

#define BOOST_POLYGON_NO_DEPS
#define BOOST_NO_USER_CONFIG
#define BOOST_NO_COMPILER_CONFIG
#define BOOST_NO_STDLIB_CONFIG
#define BOOST_NO_PLATFORM_CONFIG
#define BOOST_HAS_STDINT_H

#define __GLIBC__ 0

#define private public

#include <boost/polygon/voronoi.hpp>

namespace py = pybind11;

#define MODULE_NAME _voronoi
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#define BEACH_LINE_NODE_KEY "BeachLineNodeKey"
#define BEACH_LINE_NODE_VALUE "BeachLineNodeValue"
#define CIRCLE_EVENT_NAME "CircleEvent"
#define COMPARISON_RESULT_NAME "ComparisonResult"
#define ORIENTATION_NAME "Orientation"
#define POINT_NAME "Point"
#define SEGMENT_NAME "Segment"
#define SITE_EVENT_NAME "SiteEvent"
#define SOURCE_CATEGORY_NAME "SourceCategory"
#define VORONOI_BUILDER_NAME "VoronoiBuilder"
#define VORONOI_CELL_NAME "VoronoiCell"
#define VORONOI_DIAGRAM_NAME "VoronoiDiagram"
#define VORONOI_EDGE_NAME "VoronoiEdge"
#define VORONOI_VERTEX_NAME "VoronoiVertex"

using coordinate_t = boost::polygon::detail::int32;
using CircleEvent = boost::polygon::detail::circle_event<coordinate_t>;
using UlpComparator = boost::polygon::detail::ulp_comparison<double>;
using ComparisonResult = UlpComparator::Result;
using CTypeTraits = boost::polygon::detail::voronoi_ctype_traits<coordinate_t>;
using Point = boost::polygon::detail::point_2d<coordinate_t>;
using SiteEvent = boost::polygon::detail::site_event<coordinate_t>;
using BeachLineNodeKey = boost::polygon::detail::beach_line_node_key<SiteEvent>;
using SourceCategory = boost::polygon::SourceCategory;
using VoronoiBuilder = boost::polygon::default_voronoi_builder;
using VoronoiDiagram = boost::polygon::voronoi_diagram<double>;
using VoronoiCell = boost::polygon::voronoi_cell<double>;
using VoronoiEdge = boost::polygon::voronoi_edge<double>;
using BeachLineNodeValue =
    boost::polygon::detail::beach_line_node_data<VoronoiEdge, CircleEvent>;
using VoronoiPredicates =
    boost::polygon::detail::voronoi_predicates<CTypeTraits>;
using Orientation = VoronoiPredicates::orientation_test::Orientation;
using VoronoiVertex = boost::polygon::voronoi_vertex<double>;

static std::string bool_repr(bool value) { return py::str(py::bool_(value)); }

template <class Object>
std::string repr(const Object& object) {
  std::ostringstream stream;
  stream.precision(std::numeric_limits<double>::digits10 + 2);
  stream << object;
  return stream.str();
}

template <typename Sequence>
static void write_sequence(std::ostream& stream, const Sequence& sequence) {
  stream << "[";
  if (!sequence.empty()) {
    stream << sequence[0];
    std::for_each(std::next(std::begin(sequence)), std::end(sequence),
                  [&stream](const typename Sequence::value_type& value) {
                    stream << ", " << value;
                  });
  }
  stream << "]";
};

struct Segment {
  Point start, end;
  Segment(const Point& start_, const Point& end_) : start(start_), end(end_) {}
};

namespace boost {
namespace polygon {
namespace detail {
static bool operator==(const CircleEvent& left, const CircleEvent& right) {
  return left.x() == right.x() && left.y() == right.y() &&
         left.lower_x() == right.lower_x() &&
         left.is_active() == right.is_active();
}

static std::ostream& operator<<(std::ostream& stream,
                                const CircleEvent& event) {
  return stream << C_STR(MODULE_NAME) "." CIRCLE_EVENT_NAME "(" << event.x()
                << ", " << event.y() << ", " << event.lower_x() << ", "
                << bool_repr(event.is_active()) << ")";
}

static std::ostream& operator<<(std::ostream& stream, const Point& point) {
  return stream << C_STR(MODULE_NAME) "." POINT_NAME "(" << point.x() << ", "
                << point.y() << ")";
}

static std::ostream& operator<<(std::ostream& stream, const SiteEvent& event) {
  return stream << C_STR(MODULE_NAME) "." SITE_EVENT_NAME "(" << event.point0()
                << ", " << event.point1() << ")";
}
}  // namespace detail

static std::ostream& operator<<(std::ostream& stream,
                                const VoronoiVertex& vertex) {
  return stream << C_STR(MODULE_NAME) "." VORONOI_VERTEX_NAME "(" << vertex.x()
                << ", " << vertex.y() << ")";
}

static bool operator==(const VoronoiVertex& left, const VoronoiVertex& right) {
  return left.x() == right.x() && left.y() == right.y();
}

template <>
struct geometry_concept<Point> {
  typedef point_concept type;
};

template <>
struct point_traits<Point> {
  typedef int coordinate_type;

  static inline coordinate_type get(const Point& point, orientation_2d orient) {
    return (orient == HORIZONTAL) ? point.x() : point.y();
  }
};

template <>
struct geometry_concept<Segment> {
  typedef segment_concept type;
};

template <>
struct segment_traits<Segment> {
  typedef Segment segment_type;
  typedef Point point_type;
  typedef int coordinate_type;

  static point_type get(const segment_type& segment, direction_1d dir) {
    return dir.to_int() ? segment.end : segment.start;
  }
};
}  // namespace polygon
}  // namespace boost

static std::ostream& operator<<(std::ostream& stream, const Segment& segment) {
  return stream << C_STR(MODULE_NAME) "." SEGMENT_NAME "(" << segment.start
                << ", " << segment.end << ")";
}

static bool operator==(const Segment& left, const Segment& right) {
  return left.start == right.start && left.end == right.end;
}

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(Python binding of boost/polygon library.)pbdoc";

  py::enum_<ComparisonResult>(m, COMPARISON_RESULT_NAME)
      .value("LESS", ComparisonResult::LESS)
      .value("EQUAL", ComparisonResult::EQUAL)
      .value("MORE", ComparisonResult::MORE);

  py::enum_<Orientation>(m, ORIENTATION_NAME)
      .value("RIGHT", Orientation::RIGHT)
      .value("COLLINEAR", Orientation::COLLINEAR)
      .value("LEFT", Orientation::LEFT);

  py::enum_<SourceCategory>(m, SOURCE_CATEGORY_NAME)
      .value("SINGLE_POINT", SourceCategory::SOURCE_CATEGORY_SINGLE_POINT)
      .value("SEGMENT_START_POINT",
             SourceCategory::SOURCE_CATEGORY_SEGMENT_START_POINT)
      .value("SEGMENT_END_POINT",
             SourceCategory::SOURCE_CATEGORY_SEGMENT_END_POINT)
      .value("INITIAL_SEGMENT", SourceCategory::SOURCE_CATEGORY_INITIAL_SEGMENT)
      .value("REVERSE_SEGMENT",
             SourceCategory::SOURCE_CATEGORY_REVERSE_SEGMENT);

  py::class_<BeachLineNodeKey>(m, BEACH_LINE_NODE_KEY)
      .def(py::init<SiteEvent>(), py::arg("site"))
      .def(py::init<SiteEvent, SiteEvent>(), py::arg("left_site"),
           py::arg("right_site"))
      .def_property_readonly(
          "left_site",
          [](const BeachLineNodeKey& self) { return self.left_site(); })
      .def_property_readonly("right_site", [](const BeachLineNodeKey& self) {
        return self.right_site();
      });

  py::class_<BeachLineNodeValue>(m, BEACH_LINE_NODE_VALUE)
      .def(py::init<VoronoiEdge*>(), py::arg("edge"))
      .def_property_readonly(
          "edge", [](const BeachLineNodeValue& self) { return self.edge(); })
      .def_property_readonly(
          "circle_event",
          [](const BeachLineNodeValue& self) { return self.circle_event(); });

  py::class_<CircleEvent>(m, CIRCLE_EVENT_NAME)
      .def(py::init([](coordinate_t center_x, coordinate_t center_y,
                       coordinate_t lower_x, bool is_active = true) {
             CircleEvent result{center_x, center_y, lower_x};
             return (is_active ? result : result.deactivate());
           }),
           py::arg("center_x"), py::arg("center_y"), py::arg("lower_x"),
           py::arg("is_active") = true)
      .def(py::self == py::self)
      .def("__repr__", repr<CircleEvent>)
      .def("deactivate", &CircleEvent::deactivate)
      .def_property_readonly("center_x",
                             [](const CircleEvent& self) { return self.x(); })
      .def_property_readonly("center_y",
                             [](const CircleEvent& self) { return self.y(); })
      .def_property_readonly("is_active", &CircleEvent::is_active)
      .def_property_readonly(
          "lower_x", [](const CircleEvent& self) { return self.lower_x(); })
      .def_property_readonly("lower_y", &CircleEvent::lower_y)
      .def_property_readonly("x",
                             [](const CircleEvent& self) { return self.x(); })
      .def_property_readonly("y",
                             [](const CircleEvent& self) { return self.y(); });

  py::class_<Point>(m, POINT_NAME)
      .def(py::init<coordinate_t, coordinate_t>(), py::arg("x"), py::arg("y"))
      .def(py::self == py::self)
      .def("__lt__",
           [](const Point& self, const Point& other) {
             static VoronoiPredicates::point_comparison_predicate<Point>
                 comparator;
             return comparator(self, other);
           })
      .def("__repr__", repr<Point>)
      .def_property_readonly("x", [](const Point& self) { return self.x(); })
      .def_property_readonly("y", [](const Point& self) { return self.y(); });

  py::class_<Segment>(m, SEGMENT_NAME)
      .def(py::init<Point, Point>(), py::arg("start"), py::arg("end"))
      .def("__repr__", repr<Segment>)
      .def(py::self == py::self)
      .def_readonly("start", &Segment::start)
      .def_readonly("end", &Segment::end);

  py::class_<SiteEvent>(m, SITE_EVENT_NAME)
      .def(py::init([](const Point& start, const Point& end,
                       std::size_t sorted_index = 0,
                       std::size_t initial_index = 0, bool is_inverse = false,
                       SourceCategory source_category =
                           SourceCategory::SOURCE_CATEGORY_SINGLE_POINT) {
             return (is_inverse ? SiteEvent{end, start}.inverse()
                                : SiteEvent{start, end})
                 .sorted_index(sorted_index)
                 .initial_index(initial_index)
                 .source_category(source_category);
           }),
           py::arg("start"), py::arg("end"), py::arg("sorted_index") = 0,
           py::arg("initial_index") = 0, py::arg("is_inverse") = false,
           py::arg("source_category") =
               SourceCategory::SOURCE_CATEGORY_SINGLE_POINT)
      .def(py::self == py::self)
      .def("__repr__", repr<SiteEvent>)
      .def("inverse", &SiteEvent::inverse)
      .def_property_readonly(
          "end", [](const SiteEvent& self) { return self.point1(); })
      .def_property_readonly(
          "initial_index",
          [](const SiteEvent& self) { return self.initial_index(); })
      .def_property_readonly("is_inverse", &SiteEvent::is_inverse)
      .def_property_readonly("is_point", &SiteEvent::is_point)
      .def_property_readonly("is_segment", &SiteEvent::is_segment)
      .def_property_readonly(
          "sorted_index",
          [](const SiteEvent& self) { return self.sorted_index(); })
      .def_property_readonly(
          "source_category",
          [](const SiteEvent& self) { return self.source_category(); })
      .def_property_readonly(
          "start", [](const SiteEvent& self) { return self.point0(); });

  py::class_<VoronoiBuilder>(m, VORONOI_BUILDER_NAME)
      .def(py::init<>())
      .def("clear", &VoronoiBuilder::clear)
      .def("construct", &VoronoiBuilder::construct<VoronoiDiagram>)
      .def("insert_point", &VoronoiBuilder::insert_point)
      .def("insert_segment", &VoronoiBuilder::insert_segment)
      .def("process_circle_event",
           &VoronoiBuilder::process_circle_event<VoronoiDiagram>)
      .def("process_site_event",
           &VoronoiBuilder::process_site_event<VoronoiDiagram>)
      .def_readonly("beach_line", &VoronoiBuilder::beach_line_)
      .def_readonly("site_events", &VoronoiBuilder::site_events_);

  py::class_<VoronoiCell>(m, VORONOI_CELL_NAME)
      .def(py::init<std::size_t, SourceCategory>(), py::arg("source_index"),
           py::arg("source_category"))
      .def_property_readonly(
          "color", [](const VoronoiCell& self) { return self.color(); })
      .def_property_readonly("contains_point", &VoronoiCell::contains_point)
      .def_property_readonly("contains_segment", &VoronoiCell::contains_segment)
      .def_property_readonly(
          "incident_edge",
          [](const VoronoiCell& self) { return self.incident_edge(); })
      .def_property_readonly("is_degenerate", &VoronoiCell::is_degenerate)
      .def_property_readonly("source_index", &VoronoiCell::source_index)
      .def_property_readonly("source_category", &VoronoiCell::source_category);

  py::class_<VoronoiDiagram>(m, VORONOI_DIAGRAM_NAME)
      .def(py::init<>())
      .def("clear", &VoronoiDiagram::clear)
      .def(
          "construct",
          [](VoronoiDiagram* self, const std::vector<Point>& points,
             const std::vector<Segment>& segments) {
            boost::polygon::construct_voronoi(points.begin(), points.end(),
                                              segments.begin(), segments.end(),
                                              self);
          },
          py::arg("points"), py::arg("segments"))
      .def_property_readonly("cells", &VoronoiDiagram::cells)
      .def_property_readonly("edges", &VoronoiDiagram::edges)
      .def_property_readonly("vertices", &VoronoiDiagram::vertices);

  py::class_<VoronoiEdge, std::unique_ptr<VoronoiEdge, py::nodelete>>(
      m, VORONOI_EDGE_NAME)
      .def(py::init<bool, bool>(), py::arg("is_linear"), py::arg("is_primary"))
      .def_property_readonly(
          "cell", [](const VoronoiEdge& self) { return self.cell(); })
      .def_property_readonly(
          "color", [](const VoronoiEdge& self) { return self.color(); })
      .def_property_readonly("is_curved", &VoronoiEdge::is_curved)
      .def_property_readonly("is_finite", &VoronoiEdge::is_finite)
      .def_property_readonly("is_infinite", &VoronoiEdge::is_infinite)
      .def_property_readonly("is_linear", &VoronoiEdge::is_linear)
      .def_property_readonly("is_primary", &VoronoiEdge::is_primary)
      .def_property_readonly("is_secondary", &VoronoiEdge::is_secondary)
      .def_property_readonly(
          "next", [](const VoronoiEdge& self) { return self.next(); })
      .def_property_readonly(
          "prev", [](const VoronoiEdge& self) { return self.prev(); })
      .def_property_readonly("rot_next",
                             [](const VoronoiEdge& self) {
                               return self.prev() == nullptr ? nullptr
                                                             : self.rot_next();
                             })
      .def_property_readonly("rot_prev",
                             [](const VoronoiEdge& self) {
                               return self.prev() == nullptr ? nullptr
                                                             : self.rot_prev();
                             })
      .def_property_readonly(
          "twin", [](const VoronoiEdge& self) { return self.twin(); });

  py::class_<VoronoiVertex>(m, VORONOI_VERTEX_NAME)
      .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
      .def("__repr__", repr<VoronoiVertex>)
      .def(py::self == py::self)
      .def_property_readonly("x", &VoronoiVertex::x)
      .def_property_readonly("y", &VoronoiVertex::y);

  m.def(
      "compare_floats",
      [](double left, double right, std::uint64_t max_ulps) {
        static UlpComparator comparator;
        return comparator(left, right, max_ulps);
      },
      py::arg("left"), py::arg("right"), py::arg("max_ulps"));

  m.def("robust_cross_product", &VoronoiPredicates::robust_cross_product,
        py::arg("first_dx"), py::arg("first_dy"), py::arg("second_dx"),
        py::arg("second_dy"));

  m.def(
      "to_orientation",
      [](const Point& vertex, const Point& first_ray_point,
         const Point& second_ray_point) {
        return VoronoiPredicates::ot::eval(vertex, first_ray_point,
                                           second_ray_point);
      },
      py::arg("vertex"), py::arg("first_ray_point"),
      py::arg("second_ray_point"));

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
