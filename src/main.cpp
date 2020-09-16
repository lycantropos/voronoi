#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <sstream>
#include <stdexcept>
#include <unordered_set>

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
#define GEOMETRY_CATEGORY_NAME "GeometryCategory"
#define ORIENTATION_NAME "Orientation"
#define POINT_NAME "Point"
#define SEGMENT_NAME "Segment"
#define SITE_EVENT_NAME "SiteEvent"
#define SOURCE_CATEGORY_NAME "SourceCategory"
#define BUILDER_NAME "Builder"
#define CELL_NAME "Cell"
#define DIAGRAM_NAME "Diagram"
#define EDGE_NAME "Edge"
#define VERTEX_NAME "Vertex"

using coordinate_t = boost::polygon::detail::int32;
using Builder = boost::polygon::default_voronoi_builder;
using Diagram = boost::polygon::voronoi_diagram<double>;
using Cell = boost::polygon::voronoi_cell<double>;
using CircleEvent = boost::polygon::detail::circle_event<coordinate_t>;
using UlpComparator = boost::polygon::detail::ulp_comparison<double>;
using ComparisonResult = UlpComparator::Result;
using CTypeTraits = boost::polygon::detail::voronoi_ctype_traits<coordinate_t>;
using Edge = boost::polygon::voronoi_edge<double>;
using GeometryCategory = boost::polygon::GeometryCategory;
using Point = boost::polygon::detail::point_2d<coordinate_t>;
using SiteEvent = boost::polygon::detail::site_event<coordinate_t>;
using BeachLineNodeKey = boost::polygon::detail::beach_line_node_key<SiteEvent>;
using SourceCategory = boost::polygon::SourceCategory;
using BeachLineNodeValue =
    boost::polygon::detail::beach_line_node_data<Edge, CircleEvent>;
using Predicates = boost::polygon::detail::voronoi_predicates<CTypeTraits>;
using EventComparisonPredicate =
    Predicates::event_comparison_predicate<SiteEvent, CircleEvent>;
using Orientation = Predicates::orientation_test::Orientation;
using Vertex = boost::polygon::voronoi_vertex<double>;

static std::string bool_repr(bool value) { return py::str(py::bool_(value)); }

template <class Object>
std::string repr(const Object& object) {
  std::ostringstream stream;
  stream.precision(std::numeric_limits<double>::digits10 + 2);
  stream << object;
  return stream.str();
}

template <class Object>
static void write_pointer(std::ostream& stream, Object* value) {
  if (value == nullptr)
    stream << py::none();
  else
    stream << *value;
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

static std::size_t get_builder_site_event_index(const Builder& builder) {
  return std::min(static_cast<std::size_t>(builder.site_event_iterator_ -
                                           builder.site_events_.begin()),
                  builder.site_events_.size());
}

struct Segment {
  Point start, end;
  Segment(const Point& start_, const Point& end_) : start(start_), end(end_) {}
};

namespace boost {
namespace polygon {
static std::ostream& operator<<(std::ostream& stream,
                                const SourceCategory& source_category) {
  stream << C_STR(MODULE_NAME) "." SOURCE_CATEGORY_NAME;
  switch (source_category) {
    case SourceCategory::SOURCE_CATEGORY_SINGLE_POINT:
      stream << ".SINGLE_POINT";
      break;
    case SourceCategory::SOURCE_CATEGORY_SEGMENT_START_POINT:
      stream << ".SEGMENT_START_POINT";
      break;
    case SourceCategory::SOURCE_CATEGORY_SEGMENT_END_POINT:
      stream << ".SEGMENT_END_POINT";
      break;
    case SourceCategory::SOURCE_CATEGORY_INITIAL_SEGMENT:
      stream << ".INITIAL_SEGMENT";
      break;
    case SourceCategory::SOURCE_CATEGORY_REVERSE_SEGMENT:
      stream << ".REVERSE_SEGMENT";
      break;
    default:
      throw std::runtime_error(std::string("Unknown `SourceCategory`: ") +
                               std::to_string(source_category) + ".");
  }
  return stream;
}

static std::ostream& operator<<(std::ostream& stream, const Builder& builder) {
  stream << C_STR(MODULE_NAME) "." BUILDER_NAME "(" << builder.index_ << ", ";
  write_sequence(stream, builder.site_events_);
  return stream << ")";
}

static std::ostream& operator<<(std::ostream& stream, const Cell& cell) {
  return stream << C_STR(MODULE_NAME) "." CELL_NAME "(" << cell.source_index()
                << ", " << cell.source_category() << ")";
}

static std::ostream& operator<<(std::ostream& stream, const Vertex& vertex) {
  return stream << C_STR(MODULE_NAME) "." VERTEX_NAME "(" << vertex.x() << ", "
                << vertex.y() << ")";
}

static void write_edge_pointer(std::ostream& stream, const Edge* edge,
                               std::unordered_set<const Edge*>& cache) {
  if (edge == nullptr) {
    stream << py::none();
    return;
  }
  if (cache.find(edge) != cache.end()) {
    stream << "...";
    return;
  }
  cache.insert(edge);
  stream << C_STR(MODULE_NAME) "." EDGE_NAME "(";
  write_pointer(stream, edge->vertex0());
  stream << ", ";
  write_edge_pointer(stream, edge->twin(), cache);
  stream << ", ";
  write_edge_pointer(stream, edge->next(), cache);
  stream << ", ";
  write_edge_pointer(stream, edge->prev(), cache);
  stream << ", ";
  write_pointer(stream, edge->cell());
  stream << ", " << bool_repr(edge->is_linear()) << ", "
         << bool_repr(edge->is_primary()) << ")";
}

static std::ostream& operator<<(std::ostream& stream, const Edge& edge) {
  std::unordered_set<const Edge*> cache;
  write_edge_pointer(stream, &edge, cache);
  return stream;
}

static bool operator==(const Vertex& left, const Vertex& right) {
  static voronoi_diagram_traits<double>::vertex_equality_predicate_type
      comparator;
  return comparator(left, right);
}

static std::ostream& operator<<(std::ostream& stream, const Diagram& diagram) {
  stream << C_STR(MODULE_NAME) "." DIAGRAM_NAME "(";
  write_sequence(stream, diagram.cells_);
  stream << ", ";
  write_sequence(stream, diagram.edges_);
  stream << ", ";
  write_sequence(stream, diagram.vertices_);
  return stream << ")";
}

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
                << ", " << event.point1() << ", " << event.sorted_index()
                << ", " << event.initial_index() << ", "
                << bool_repr(event.is_inverse()) << ", "
                << event.source_category() << ")";
}
}  // namespace detail

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

  py::enum_<GeometryCategory>(m, GEOMETRY_CATEGORY_NAME)
      .value("POINT", GeometryCategory::GEOMETRY_CATEGORY_POINT)
      .value("SEGMENT", GeometryCategory::GEOMETRY_CATEGORY_SEGMENT);

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
      .value("REVERSE_SEGMENT", SourceCategory::SOURCE_CATEGORY_REVERSE_SEGMENT)
      .def("belongs", &boost::polygon::belongs);

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
      .def(py::init<Edge*>(), py::arg("edge"))
      .def_property_readonly(
          "edge", [](const BeachLineNodeValue& self) { return self.edge(); })
      .def_property_readonly(
          "circle_event",
          [](const BeachLineNodeValue& self) { return self.circle_event(); });

  py::class_<Builder>(m, BUILDER_NAME)
      .def(py::init([](std::size_t index,
                       const std::vector<SiteEvent>& site_events) {
             auto result = std::make_unique<Builder>();
             result->index_ = index;
             result->site_events_ = site_events;
             return result;
           }),
           py::arg("index") = 0,
           py::arg("site_events") = std::vector<SiteEvent>{})
      .def("__repr__", repr<Builder>)
      .def("clear", &Builder::clear)
      .def("construct", &Builder::construct<Diagram>, py::arg("diagram"))
      .def("init_sites_queue", &Builder::init_sites_queue)
      .def("insert_point", &Builder::insert_point, py::arg("x"), py::arg("y"))
      .def("insert_segment", &Builder::insert_segment, py::arg("start_x"),
           py::arg("start_y"), py::arg("end_x"), py::arg("end_y"))
      .def("process_circle_event", &Builder::process_circle_event<Diagram>,
           py::arg("diagram"))
      .def("process_site_event", &Builder::process_site_event<Diagram>,
           py::arg("diagram"))
      .def_property_readonly("site_event_index", get_builder_site_event_index)
      .def_readonly("beach_line", &Builder::beach_line_)
      .def_readonly("index", &Builder::index_)
      .def_readonly("site_events", &Builder::site_events_);

  py::class_<Cell, std::unique_ptr<Cell, py::nodelete>>(m, CELL_NAME)
      .def(py::init([](std::size_t source_index, SourceCategory source_category,
                       Edge* incident_edge) {
             Cell result{source_index, source_category};
             result.incident_edge(incident_edge);
             return result;
           }),
           py::arg("source_index"), py::arg("source_category"),
           py::arg("incident_edge") = nullptr)
      .def("__repr__", repr<Cell>)
      .def_property_readonly("contains_point", &Cell::contains_point)
      .def_property_readonly("contains_segment", &Cell::contains_segment)
      .def_property_readonly(
          "incident_edge",
          [](const Cell& self) { return self.incident_edge(); })
      .def_property_readonly("is_degenerate", &Cell::is_degenerate)
      .def_property_readonly("source_index", &Cell::source_index)
      .def_property_readonly("source_category", &Cell::source_category);

  py::class_<CircleEvent>(m, CIRCLE_EVENT_NAME)
      .def(py::init([](coordinate_t center_x, coordinate_t center_y,
                       coordinate_t lower_x, bool is_active) {
             CircleEvent result{center_x, center_y, lower_x};
             return (is_active ? result : result.deactivate());
           }),
           py::arg("center_x"), py::arg("center_y"), py::arg("lower_x"),
           py::arg("is_active") = true)
      .def(py::self == py::self)
      .def("__lt__",
           [](const CircleEvent& self, const CircleEvent& other) {
             static EventComparisonPredicate comparator;
             return comparator(self, other);
           })
      .def("__lt__",
           [](const CircleEvent& self, const SiteEvent& other) {
             static EventComparisonPredicate comparator;
             return comparator(self, other);
           })
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

  py::class_<Diagram>(m, DIAGRAM_NAME)
      .def(py::init([](const std::vector<Cell>& cells,
                       const std::vector<Edge>& edges,
                       const std::vector<Vertex>& vertices) {
             auto result = std::make_unique<Diagram>();
             result->cells_ = cells;
             result->edges_ = edges;
             result->vertices_ = vertices;
             return result;
           }),
           py::arg("cells") = std::vector<Cell>{},
           py::arg("edges") = std::vector<Edge>{},
           py::arg("vertices") = std::vector<Vertex>{})
      .def("__repr__", repr<Diagram>)
      .def("clear", &Diagram::clear)
      .def(
          "construct",
          [](Diagram* self, const std::vector<Point>& points,
             const std::vector<Segment>& segments) {
            boost::polygon::construct_voronoi(points.begin(), points.end(),
                                              segments.begin(), segments.end(),
                                              self);
          },
          py::arg("points"), py::arg("segments"))
      .def("is_primary_edge", &Diagram::is_primary_edge<SiteEvent>,
           py::arg("first_event"), py::arg("second_event"))
      .def("remove_edge", &Diagram::remove_edge, py::arg("edge").none(false))
      .def("_build", &Diagram::_build)
      .def("_process_single_site", &Diagram::_process_single_site<coordinate_t>,
           py::arg("site"))
      .def_property_readonly("cells", &Diagram::cells)
      .def_property_readonly("edges", &Diagram::edges)
      .def_property_readonly("vertices", &Diagram::vertices);

  py::class_<Edge, std::unique_ptr<Edge, py::nodelete>>(m, EDGE_NAME)
      .def(py::init([](Vertex* start, Edge* twin, Edge* prev, Edge* next,
                       Cell* cell, bool is_linear, bool is_primary) {
             Edge result{is_linear, is_primary};
             result.vertex0(start);
             result.twin(twin);
             result.prev(prev);
             result.next(next);
             result.cell(cell);
             return result;
           }),
           py::arg("start"), py::arg("twin"), py::arg("prev"), py::arg("next"),
           py::arg("cell"), py::arg("is_linear"), py::arg("is_primary"))
      .def("__repr__", repr<Edge>)
      .def_property_readonly("cell",
                             [](const Edge& self) { return self.cell(); })
      .def_property_readonly("end",
                             [](const Edge& self) {
                               return self.twin() == nullptr ? nullptr
                                                             : self.vertex1();
                             })
      .def_property_readonly("is_curved", &Edge::is_curved)
      .def_property_readonly("is_finite", &Edge::is_finite)
      .def_property_readonly("is_infinite", &Edge::is_infinite)
      .def_property_readonly("is_linear", &Edge::is_linear)
      .def_property_readonly("is_primary", &Edge::is_primary)
      .def_property_readonly("is_secondary", &Edge::is_secondary)
      .def_property_readonly("next",
                             [](const Edge& self) { return self.next(); })
      .def_property_readonly("prev",
                             [](const Edge& self) { return self.prev(); })
      .def_property_readonly("rot_next",
                             [](const Edge& self) {
                               return self.prev() == nullptr ? nullptr
                                                             : self.rot_next();
                             })
      .def_property_readonly("rot_prev",
                             [](const Edge& self) {
                               return self.prev() == nullptr ? nullptr
                                                             : self.rot_prev();
                             })
      .def_property_readonly("start",
                             [](const Edge& self) { return self.vertex0(); })
      .def_property_readonly("twin",
                             [](const Edge& self) { return self.twin(); });

  py::class_<Point>(m, POINT_NAME)
      .def(py::init<coordinate_t, coordinate_t>(), py::arg("x"), py::arg("y"))
      .def(py::self == py::self)
      .def("__lt__",
           [](const Point& self, const Point& other) {
             static Predicates::point_comparison_predicate<Point> comparator;
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
                       std::size_t sorted_index, std::size_t initial_index,
                       bool is_inverse, SourceCategory source_category) {
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
      .def("__lt__",
           [](const SiteEvent& self, const CircleEvent& other) {
             static EventComparisonPredicate comparator;
             return comparator(self, other);
           })
      .def("__lt__",
           [](const SiteEvent& self, const SiteEvent& other) {
             static EventComparisonPredicate comparator;
             return comparator(self, other);
           })
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
          "is_vertical",
          [](const SiteEvent& self) { return Predicates::is_vertical(self); })
      .def_property_readonly(
          "sorted_index",
          [](const SiteEvent& self) { return self.sorted_index(); })
      .def_property_readonly(
          "source_category",
          [](const SiteEvent& self) { return self.source_category(); })
      .def_property_readonly(
          "start", [](const SiteEvent& self) { return self.point0(); });

  py::class_<Vertex, std::unique_ptr<Vertex, py::nodelete>>(m, VERTEX_NAME)
      .def(py::init([](double x, double y, Edge* incident_edge) {
             Vertex result{x, y};
             result.incident_edge(incident_edge);
             return result;
           }),
           py::arg("x"), py::arg("y"), py::arg("incident_edge") = nullptr)
      .def("__repr__", repr<Vertex>)
      .def(py::self == py::self)
      .def_property_readonly(
          "incident_edge",
          [](const Vertex& self) { return self.incident_edge(); })
      .def_property_readonly("is_degenerate", &Vertex::is_degenerate)
      .def_property_readonly("x", &Vertex::x)
      .def_property_readonly("y", &Vertex::y);

  m.def(
      "compare_floats",
      [](double left, double right, std::uint64_t max_ulps) {
        static UlpComparator comparator;
        return comparator(left, right, max_ulps);
      },
      py::arg("left"), py::arg("right"), py::arg("max_ulps"));

  m.def("robust_cross_product", &Predicates::robust_cross_product,
        py::arg("first_dx"), py::arg("first_dy"), py::arg("second_dx"),
        py::arg("second_dy"));

  m.def(
      "to_orientation",
      [](const Point& vertex, const Point& first_ray_point,
         const Point& second_ray_point) {
        return Predicates::ot::eval(vertex, first_ray_point, second_ray_point);
      },
      py::arg("vertex"), py::arg("first_ray_point"),
      py::arg("second_ray_point"));

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
