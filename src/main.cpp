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
#define BEACH_LINE_KEY_NAME "BeachLineKey"
#define BEACH_LINE_VALUE_NAME "BeachLineValue"
#define BIG_FLOAT_NAME "BigFloat"
#define BIG_INT_NAME "BigInt"
#define CIRCLE_EVENT_NAME "CircleEvent"
#define COMPARISON_RESULT_NAME "ComparisonResult"
#define GEOMETRY_CATEGORY_NAME "GeometryCategory"
#define ORIENTATION_NAME "Orientation"
#define POINT_NAME "Point"
#define ROBUST_DIFFERENCE_NAME "RobustDifference"
#define ROBUST_FLOAT_NAME "RobustFloat"
#define SEGMENT_NAME "Segment"
#define SITE_EVENT_NAME "SiteEvent"
#define SOURCE_CATEGORY_NAME "SourceCategory"
#define BUILDER_NAME "Builder"
#define CELL_NAME "Cell"
#define DIAGRAM_NAME "Diagram"
#define EDGE_NAME "Edge"
#define VERTEX_NAME "Vertex"
#ifndef VERSION_INFO
#define VERSION_INFO "dev"
#endif

using coordinate_t = boost::polygon::detail::int32;
using Builder = boost::polygon::default_voronoi_builder;
using Diagram = boost::polygon::voronoi_diagram<double>;
using Cell = boost::polygon::voronoi_cell<double>;
using CircleEvent = boost::polygon::detail::circle_event<double>;
using UlpComparator = boost::polygon::detail::ulp_comparison<double>;
using ComparisonResult = UlpComparator::Result;
using CTypeTraits = boost::polygon::detail::voronoi_ctype_traits<coordinate_t>;
using BigFloat = CTypeTraits::efpt_type;
using BigInt = CTypeTraits::big_int_type;
using Edge = boost::polygon::voronoi_edge<double>;
using GeometryCategory = boost::polygon::GeometryCategory;
using Point = boost::polygon::detail::point_2d<coordinate_t>;
using RobustFloat = boost::polygon::detail::robust_fpt<double>;
using RobustDifference = boost::polygon::detail::robust_dif<RobustFloat>;
using RobustSumExpression = boost::polygon::detail::robust_sqrt_expr<
    BigInt, BigFloat, boost::polygon::detail::type_converter_efpt>;
using SiteEvent = boost::polygon::detail::site_event<coordinate_t>;
using BeachLineKey = boost::polygon::detail::beach_line_node_key<SiteEvent>;
using SourceCategory = boost::polygon::SourceCategory;
using BeachLineValue =
    boost::polygon::detail::beach_line_node_data<Edge, CircleEvent>;
using Predicates = boost::polygon::detail::voronoi_predicates<CTypeTraits>;
using EventComparisonPredicate =
    Predicates::event_comparison_predicate<SiteEvent, CircleEvent>;
using Orientation = Predicates::orientation_test::Orientation;
using Vertex = boost::polygon::voronoi_vertex<double>;

static int to_sign(coordinate_t value) {
  return value > 0 ? 1 : (value < 0 ? -1 : 0);
}

static std::string bool_repr(bool value) { return value ? "True" : "False"; }

template <class Object>
std::string to_repr(const Object& object) {
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

struct Segment {
  Point start, end;
  Segment(const Point& start_, const Point& end_) : start(start_), end(end_) {}
};

namespace boost {
namespace polygon {
static std::ostream& operator<<(std::ostream& stream,
                                const SourceCategory& source_category) {
  stream << C_STR(MODULE_NAME) "." SOURCE_CATEGORY_NAME ".";
  switch (source_category) {
    case SourceCategory::SOURCE_CATEGORY_SINGLE_POINT:
      stream << "SINGLE_POINT";
      break;
    case SourceCategory::SOURCE_CATEGORY_SEGMENT_START_POINT:
      stream << "SEGMENT_START_POINT";
      break;
    case SourceCategory::SOURCE_CATEGORY_SEGMENT_END_POINT:
      stream << "SEGMENT_END_POINT";
      break;
    case SourceCategory::SOURCE_CATEGORY_INITIAL_SEGMENT:
      stream << "INITIAL_SEGMENT";
      break;
    case SourceCategory::SOURCE_CATEGORY_REVERSE_SEGMENT:
      stream << "REVERSE_SEGMENT";
      break;
    default:
      stream << "???";
      break;
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

static std::ostream& operator<<(std::ostream& stream, const Edge& edge) {
  stream << C_STR(MODULE_NAME) "." EDGE_NAME "(";
  write_pointer(stream, edge.vertex0());
  stream << ", ";
  write_pointer(stream, edge.cell());
  return stream << ", " << bool_repr(edge.is_linear()) << ", "
                << bool_repr(edge.is_primary()) << ")";
}

static bool operator==(const Vertex& left, const Vertex& right) {
  static const voronoi_diagram_traits<double>::vertex_equality_predicate_type
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
static std::ostream& operator<<(std::ostream& stream, const BigFloat& float_) {
  return stream << C_STR(MODULE_NAME) "." BIG_FLOAT_NAME "(" << float_.val_
                << ", " << float_.exp_ << ")";
}

static std::ostream& operator<<(std::ostream& stream, const BigInt& int_) {
  stream << C_STR(MODULE_NAME) "." BIG_INT_NAME "(" << to_sign(int_.count())
         << ", [";
  std::size_t size = int_.size();
  const auto& chunks = int_.chunks();
  if (size != 0) {
    stream << chunks[0];
    for (std::size_t index = 1; index < size; ++index)
      stream << ", " << chunks[index];
  }
  return stream << "])";
}

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

static std::ostream& operator<<(std::ostream& stream,
                                const RobustFloat& float_) {
  return stream << C_STR(MODULE_NAME) "." ROBUST_FLOAT_NAME "(" << float_.fpv()
                << ", " << float_.re() << ")";
}

static std::ostream& operator<<(std::ostream& stream,
                                const RobustDifference& difference) {
  return stream << C_STR(MODULE_NAME) "." ROBUST_DIFFERENCE_NAME "("
                << difference.pos() << ", " << difference.neg() << ")";
}

static std::ostream& operator<<(std::ostream& stream, const SiteEvent& event) {
  return stream << C_STR(MODULE_NAME) "." SITE_EVENT_NAME "(" << event.point0()
                << ", " << event.point1() << ", " << event.sorted_index()
                << ", " << event.initial_index() << ", "
                << bool_repr(event.is_inverse()) << ", "
                << event.source_category() << ")";
}

static std::ostream& operator<<(std::ostream& stream, const BeachLineKey& key) {
  return stream << C_STR(MODULE_NAME) "." BEACH_LINE_KEY_NAME "("
                << key.left_site() << ", " << key.right_site() << ")";
}

static std::ostream& operator<<(std::ostream& stream,
                                const BeachLineValue& value) {
  stream << C_STR(MODULE_NAME) "." BEACH_LINE_VALUE_NAME "(";
  write_pointer(stream, value.edge());
  stream << ", ";
  write_pointer(stream, value.circle_event());
  return stream << ")";
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
  m.attr("__version__") = C_STR(VERSION_INFO);

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

  py::class_<BeachLineKey>(m, BEACH_LINE_KEY_NAME)
      .def(py::init<SiteEvent>(), py::arg("site"))
      .def(py::init<SiteEvent, SiteEvent>(), py::arg("left_site"),
           py::arg("right_site"))
      .def("__repr__", to_repr<BeachLineKey>)
      .def(
          "__lt__",
          [](const BeachLineKey& self, const BeachLineKey& other) {
            static const Predicates::node_comparison_predicate<BeachLineKey>
                comparator;
            return comparator(self, other);
          },
          py::is_operator())
      .def(
          "to_comparison_y",
          [](const BeachLineKey& self, bool is_new_node) {
            static const Predicates::node_comparison_predicate<BeachLineKey>
                comparator;
            return comparator.get_comparison_y(self, is_new_node);
          },
          py::arg("is_new_node") = true)
      .def_property_readonly(
          "comparison_site",
          [](const BeachLineKey& self) {
            static const Predicates::node_comparison_predicate<BeachLineKey>
                comparator;
            return comparator.get_comparison_site(self);
          })
      .def_property_readonly(
          "left_site",
          [](const BeachLineKey& self) { return self.left_site(); })
      .def_property_readonly("right_site", [](const BeachLineKey& self) {
        return self.right_site();
      });

  py::class_<BeachLineValue>(m, BEACH_LINE_VALUE_NAME)
      .def(py::init([](Edge* edge, CircleEvent* circle_event) {
             return BeachLineValue{edge}.circle_event(circle_event);
           }),
           py::arg("edge"), py::arg("circle_event") = nullptr)
      .def("__repr__", to_repr<BeachLineValue>)
      .def_property_readonly(
          "edge", [](const BeachLineValue& self) { return self.edge(); })
      .def_property_readonly("circle_event", [](const BeachLineValue& self) {
        return self.circle_event();
      });

  py::class_<BigFloat>(m, BIG_FLOAT_NAME)
      .def(py::init<double, int>(), py::arg("mantissa"), py::arg("exponent"))
      .def(-py::self)
      .def(py::self + py::self)
      .def(py::self - py::self)
      .def(py::self * py::self)
      .def(py::self / py::self)
      .def(py::self += py::self)
      .def(py::self -= py::self)
      .def(py::self *= py::self)
      .def(py::self /= py::self)
      .def("__bool__",
           [](const BigFloat& self) {
             return !boost::polygon::detail::is_zero(self);
           })
      .def("__float__", &BigFloat::d)
      .def("__repr__", to_repr<BigFloat>)
      .def("sqrt", &BigFloat::sqrt)
      .def_readonly("exponent", &BigFloat::exp_)
      .def_readonly("mantissa", &BigFloat::val_);

  py::class_<BigInt>(m, BIG_INT_NAME)
      .def(py::init<boost::polygon::detail::int64>(), py::arg("value"))
      .def(py::init<>(
               [](std::int8_t sign, const std::vector<std::uint32_t>& digits) {
                 auto result = std::make_unique<BigInt>();
                 result->count_ = to_sign(sign) * digits.size();
                 std::copy(digits.begin(), digits.end(), result->chunks_);
                 return result;
               }),
           py::arg("sign"), py::arg("digits"))
      .def(-py::self)
      .def(py::self + py::self)
      .def(py::self - py::self)
      .def(py::self * py::self)
      .def(py::self + coordinate_t())
      .def(py::self - coordinate_t())
      .def(py::self * coordinate_t())
      .def("__bool__",
           [](const BigInt& self) {
             return !boost::polygon::detail::is_zero(self);
           })
      .def("__float__", &BigInt::d)
      .def("__repr__", to_repr<BigInt>)
      .def("frexp", &BigInt::p)
      .def_property_readonly(
          "digits",
          [](const BigInt& self) -> std::vector<std::uint32_t> {
            std::size_t size = self.size();
            std::vector<std::uint32_t> result;
            const auto& chunks = self.chunks();
            for (std::size_t index = 0; index < size; ++index)
              result.push_back(chunks[index]);
            return result;
          })
      .def_property_readonly("sign", [](const BigInt& self) {
        const auto count = self.count();
        return to_sign(count);
      });

  py::class_<Builder>(m, BUILDER_NAME)
      .def(py::init([](std::size_t index,
                       const std::vector<SiteEvent>& site_events) {
             auto result = std::make_unique<Builder>();
             result->index_ = index;
             result->site_events_ = site_events;
             result->site_event_index_ =
                 std::numeric_limits<std::size_t>::max();
             return result;
           }),
           py::arg("index") = 0,
           py::arg("site_events") = std::vector<SiteEvent>{})
      .def("__repr__", to_repr<Builder>)
      .def("clear", &Builder::clear)
      .def("construct", &Builder::construct<Diagram>, py::arg("diagram"))
      .def("init_beach_line", &Builder::init_beach_line<Diagram>,
           py::arg("diagram"))
      .def("init_sites_queue", &Builder::init_sites_queue)
      .def("insert_new_arc",
           [](Builder& self, const SiteEvent& arc_first_site,
              const SiteEvent& arc_second_site, const SiteEvent& site,
              Diagram* diagram) {
             self.insert_new_arc(arc_first_site, arc_second_site, site,
                                 self.beach_line_.end(), diagram);
           })
      .def(
          "insert_point",
          [](Builder* builder, const Point& point) {
            return boost::polygon::insert(point, builder);
          },
          py::arg("point"))
      .def(
          "insert_segment",
          [](Builder* builder, const Segment& segment) {
            return boost::polygon::insert(segment, builder);
          },
          py::arg("segment"))
      .def("process_circle_event", &Builder::process_circle_event<Diagram>,
           py::arg("diagram"))
      .def("process_site_event", &Builder::process_site_event<Diagram>,
           py::arg("diagram"))
      .def_property_readonly(
          "beach_line",
          [](Builder& self) {
            std::vector<std::pair<BeachLineKey, BeachLineValue>> result;
            for (auto& item : self.beach_line_) {
              auto& value = item.second;
              result.push_back(
                  {item.first, BeachLineValue{static_cast<Edge*>(value.edge())}
                                   .circle_event(value.circle_event())});
            }
            return result;
          })
      .def_property_readonly(
          "end_points",
          [](const Builder& self) {
            auto queue = self.end_points_;
            std::vector<
                std::pair<Point, std::pair<BeachLineKey, BeachLineValue>>>
                result;
            while (!queue.empty()) {
              const auto element = queue.top();
              auto raw_value = element.second->second;
              result.push_back(
                  {element.first,
                   {element.second->first,
                    BeachLineValue(static_cast<Edge*>(raw_value.edge()))
                        .circle_event(raw_value.circle_event())}});
              queue.pop();
            }
            return result;
          })
      .def_property_readonly(
          "site_event_index",
          [](const Builder& self) {
            return self.site_event_index_ ==
                           std::numeric_limits<std::size_t>::max()
                       ? self.site_events_.size()
                       : self.site_event_index_;
          })
      .def_readonly("index", &Builder::index_)
      .def_readonly("site_events", &Builder::site_events_);

  py::class_<Cell, std::unique_ptr<Cell, py::nodelete>>(m, CELL_NAME)
      .def(py::init<std::size_t, SourceCategory>(), py::arg("source_index"),
           py::arg("source_category"))
      .def("__repr__", to_repr<Cell>)
      .def_property_readonly("contains_point", &Cell::contains_point)
      .def_property_readonly("contains_segment", &Cell::contains_segment)
      .def_property(
          "incident_edge",
          [](const Cell& self) { return self.incident_edge(); },
          [](Cell& self, Edge* value) { self.incident_edge(value); })
      .def_property_readonly("is_degenerate", &Cell::is_degenerate)
      .def_property_readonly("source_index", &Cell::source_index)
      .def_property_readonly("source_category", &Cell::source_category);

  py::class_<CircleEvent, std::unique_ptr<CircleEvent, py::nodelete>>(
      m, CIRCLE_EVENT_NAME)
      .def(py::init([](double center_x, double center_y, double lower_x,
                       bool is_active) {
             CircleEvent result{center_x, center_y, lower_x};
             return (is_active ? result : result.deactivate());
           }),
           py::arg("center_x"), py::arg("center_y"), py::arg("lower_x"),
           py::arg("is_active") = true)
      .def(py::self == py::self)
      .def(
          "__lt__",
          [](const CircleEvent& self, const CircleEvent& other) {
            static const EventComparisonPredicate comparator;
            return comparator(self, other);
          },
          py::is_operator())
      .def(
          "__lt__",
          [](const CircleEvent& self, const SiteEvent& other) {
            static const EventComparisonPredicate comparator;
            return comparator(self, other);
          },
          py::is_operator())
      .def("__repr__", to_repr<CircleEvent>)
      .def("deactivate", &CircleEvent::deactivate)
      .def("lies_outside_vertical_segment",
           [](const CircleEvent& self, const SiteEvent& site) {
             static Predicates::circle_formation_predicate<SiteEvent,
                                                           CircleEvent>
                 predicate;
             return predicate.lies_outside_vertical_segment(self, site);
           })
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
      .def("__repr__", to_repr<Diagram>)
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
      .def("is_linear_edge", &Diagram::is_linear_edge<SiteEvent>,
           py::arg("first_event"), py::arg("second_event"))
      .def("is_primary_edge", &Diagram::is_primary_edge<SiteEvent>,
           py::arg("first_event"), py::arg("second_event"))
      .def("remove_edge", &Diagram::remove_edge, py::arg("edge").none(false))
      .def("_build", &Diagram::_build)
      .def(
          "_insert_new_edge",
          [](Diagram& self, const SiteEvent& first_event,
             const SiteEvent& second_event) {
            auto result = self._insert_new_edge(first_event, second_event);
            return std::make_pair(static_cast<Edge*>(result.first),
                                  static_cast<Edge*>(result.second));
          },
          py::arg("first_event"), py::arg("second_event"))
      .def(
          "_insert_new_edge_from_intersection",
          [](Diagram& self, const SiteEvent& first_site_event,
             const SiteEvent& second_site_event,
             const CircleEvent& circle_event, Edge* first_bisector,
             Edge* second_bisector) {
            auto result = self._insert_new_edge(
                first_site_event, second_site_event, circle_event,
                first_bisector, second_bisector);
            return std::make_pair(static_cast<Edge*>(result.first),
                                  static_cast<Edge*>(result.second));
          },
          py::arg("first_site_event"), py::arg("second_site_event"),
          py::arg("circle_event"), py::arg("first_bisector"),
          py::arg("second_bisector"))
      .def("_process_single_site", &Diagram::_process_single_site<coordinate_t>,
           py::arg("site"))
      .def("_reserve", &Diagram::_reserve, py::arg("sites_count"))
      .def_property_readonly("cells", &Diagram::cells)
      .def_property_readonly("edges", &Diagram::edges)
      .def_property_readonly("vertices", &Diagram::vertices);

  py::class_<Edge, std::unique_ptr<Edge, py::nodelete>>(m, EDGE_NAME)
      .def(py::init(
               [](Vertex* start, Cell* cell, bool is_linear, bool is_primary) {
                 Edge result{is_linear, is_primary};
                 result.vertex0(start);
                 result.cell(cell);
                 return result;
               }),
           py::arg("start"), py::arg("cell").none(false), py::arg("is_linear"),
           py::arg("is_primary"))
      .def("__repr__", to_repr<Edge>)
      .def_property_readonly("cell",
                             [](const Edge& self) { return self.cell(); })
      .def_property_readonly("end",
                             [](const Edge& self) {
                               return self.twin() == nullptr ? nullptr
                                                             : self.vertex1();
                             })
      .def_property_readonly("is_curved", &Edge::is_curved)
      .def_property_readonly("is_finite",
                             [](const Edge& self) {
                               return self.twin() == nullptr ? false
                                                             : self.is_finite();
                             })
      .def_property_readonly(
          "is_infinite",
          [](const Edge& self) {
            return self.twin() == nullptr ? true : self.is_infinite();
          })
      .def_property_readonly("is_linear", &Edge::is_linear)
      .def_property_readonly("is_primary", &Edge::is_primary)
      .def_property_readonly("is_secondary", &Edge::is_secondary)
      .def_property(
          "next", [](const Edge& self) { return self.next(); },
          [](Edge& self, Edge* value) { self.next(value); })
      .def_property(
          "prev", [](const Edge& self) { return self.prev(); },
          [](Edge& self, Edge* value) { self.prev(value); })
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
      .def_property(
          "twin", [](const Edge& self) { return self.twin(); },
          [](Edge& self, Edge* value) { self.twin(value); });

  py::class_<Point>(m, POINT_NAME)
      .def(py::init<coordinate_t, coordinate_t>(), py::arg("x"), py::arg("y"))
      .def(py::self == py::self)
      .def(
          "__lt__",
          [](const Point& self, const Point& other) {
            static const Predicates::point_comparison_predicate<Point>
                comparator;
            return comparator(self, other);
          },
          py::is_operator())
      .def("__repr__", to_repr<Point>)
      .def_property_readonly("x", [](const Point& self) { return self.x(); })
      .def_property_readonly("y", [](const Point& self) { return self.y(); });

  py::class_<RobustFloat>(m, ROBUST_FLOAT_NAME)
      .def(py::init<>())
      .def(py::init<double>(), py::arg("value"))
      .def(py::init<double, double>(), py::arg("value"),
           py::arg("relative_error"))
      .def(-py::self)
      .def(py::self + py::self)
      .def(py::self - py::self)
      .def(py::self * py::self)
      .def(py::self / py::self)
      .def(py::self += py::self)
      .def(py::self -= py::self)
      .def(py::self *= py::self)
      .def(py::self /= py::self)
      .def("__bool__",
           [](const RobustFloat& self) {
             return !boost::polygon::detail::is_zero(self);
           })
      .def("__repr__", to_repr<RobustFloat>)
      .def("sqrt", &RobustFloat::sqrt)
      .def_property_readonly("value", &RobustFloat::fpv)
      .def_property_readonly("relative_error", &RobustFloat::re);

  py::class_<RobustDifference>(m, ROBUST_DIFFERENCE_NAME)
      .def(py::init<>())
      .def(py::init<RobustFloat, RobustFloat>(), py::arg("minuend"),
           py::arg("subtrahend"))
      .def(-py::self)
      .def(py::self + RobustFloat())
      .def(py::self - RobustFloat())
      .def(py::self * RobustFloat())
      .def(py::self / RobustFloat())
      .def(py::self += RobustFloat())
      .def(py::self -= RobustFloat())
      .def(py::self *= RobustFloat())
      .def(py::self /= RobustFloat())
      .def(py::self + RobustDifference())
      .def(py::self - RobustDifference())
      .def(py::self * RobustDifference())
      .def(py::self += RobustDifference())
      .def(py::self -= RobustDifference())
      .def(py::self *= RobustDifference())
      .def("__repr__", to_repr<RobustDifference>)
      .def("evaluate", &RobustDifference::dif)
      .def_property_readonly("minuend", &RobustDifference::pos)
      .def_property_readonly("subtrahend", &RobustDifference::neg);

  py::class_<Segment>(m, SEGMENT_NAME)
      .def(py::init<Point, Point>(), py::arg("start"), py::arg("end"))
      .def("__repr__", to_repr<Segment>)
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
      .def(
          "__lt__",
          [](const SiteEvent& self, const CircleEvent& other) {
            static const EventComparisonPredicate comparator;
            return comparator(self, other);
          },
          py::is_operator())
      .def(
          "__lt__",
          [](const SiteEvent& self, const SiteEvent& other) {
            static const EventComparisonPredicate comparator;
            return comparator(self, other);
          },
          py::is_operator())
      .def("__repr__", to_repr<SiteEvent>)
      .def_property_readonly(
          "comparison_point",
          [](const SiteEvent& self) {
            static const Predicates::node_comparison_predicate<BeachLineKey>
                comparator;
            return comparator.get_comparison_point(self);
          })
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
      .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
      .def("__repr__", to_repr<Vertex>)
      .def(py::self == py::self)
      .def_property(
          "incident_edge",
          [](const Vertex& self) { return self.incident_edge(); },
          [](Vertex& self, Edge* value) { self.incident_edge(value); })
      .def_property_readonly("is_degenerate", &Vertex::is_degenerate)
      .def_property_readonly("x", &Vertex::x)
      .def_property_readonly("y", &Vertex::y);

  m.def(
      "compare_floats",
      [](double left, double right, unsigned int max_ulps) {
        static const UlpComparator comparator;
        return comparator(left, right, max_ulps);
      },
      py::arg("left"), py::arg("right"), py::arg("max_ulps"));

  m.def(
      "compute_circle_event",
      [](CircleEvent& circle_event, const SiteEvent& first_site,
         const SiteEvent& second_site, const SiteEvent& third_site) {
        static Predicates::circle_formation_predicate<SiteEvent, CircleEvent>
            predicate;
        return predicate(first_site, second_site, third_site, circle_event);
      },
      py::arg("circle_event"), py::arg("first_site"), py::arg("second_site"),
      py::arg("third_site"));

  m.def(
      "compute_point_point_point_circle_event",
      [](CircleEvent& circle_event, const SiteEvent& first_site,
         const SiteEvent& second_site, const SiteEvent& third_site) {
        static Predicates::lazy_circle_formation_functor<SiteEvent, CircleEvent>
            functor;
        functor.ppp(first_site, second_site, third_site, circle_event);
      },
      py::arg("circle_event"), py::arg("first_site"), py::arg("second_site"),
      py::arg("third_site"));

  m.def(
      "compute_point_point_segment_circle_event",
      [](CircleEvent& circle_event, const SiteEvent& first_site,
         const SiteEvent& second_site, const SiteEvent& third_site,
         int segment_index) {
        static Predicates::lazy_circle_formation_functor<SiteEvent, CircleEvent>
            functor;
        functor.pps(first_site, second_site, third_site, segment_index,
                    circle_event);
      },
      py::arg("circle_event"), py::arg("first_site"), py::arg("second_site"),
      py::arg("third_site"), py::arg("segment_index"));

  m.def(
      "compute_point_segment_segment_circle_event",
      [](CircleEvent& circle_event, const SiteEvent& first_site,
         const SiteEvent& second_site, const SiteEvent& third_site,
         int point_index) {
        static Predicates::lazy_circle_formation_functor<SiteEvent, CircleEvent>
            functor;
        functor.pss(first_site, second_site, third_site, point_index,
                    circle_event);
      },
      py::arg("circle_event"), py::arg("first_site"), py::arg("second_site"),
      py::arg("third_site"), py::arg("point_index"));

  m.def(
      "compute_segment_segment_segment_circle_event",
      [](CircleEvent& circle_event, const SiteEvent& first_site,
         const SiteEvent& second_site, const SiteEvent& third_site) {
        static Predicates::lazy_circle_formation_functor<SiteEvent, CircleEvent>
            functor;
        functor.sss(first_site, second_site, third_site, circle_event);
      },
      py::arg("circle_event"), py::arg("first_site"), py::arg("second_site"),
      py::arg("third_site"));

  m.def(
      "distance_to_point_arc",
      [](const SiteEvent& site, const Point& point) {
        static const Predicates::distance_predicate<SiteEvent> comparator;
        return comparator.find_distance_to_point_arc(site, point);
      },
      py::arg("site"), py::arg("point"));

  m.def(
      "distance_to_segment_arc",
      [](const SiteEvent& site, const Point& point) {
        static const Predicates::distance_predicate<SiteEvent> comparator;
        return comparator.find_distance_to_segment_arc(site, point);
      },
      py::arg("site"), py::arg("point"));

  m.def(
      "horizontal_goes_through_right_arc_first",
      [](const SiteEvent& left_site, const SiteEvent& right_site,
         const Point& point) {
        static const Predicates::distance_predicate<SiteEvent> comparator;
        return comparator(left_site, right_site, point);
      },
      py::arg("left_site"), py::arg("right_site"), py::arg("point"));

  m.def(
      "point_point_horizontal_goes_through_right_arc_first",
      [](const SiteEvent& left_site, const SiteEvent& right_site,
         const Point& point) {
        static const Predicates::distance_predicate<SiteEvent> comparator;
        return comparator.pp(left_site, right_site, point);
      },
      py::arg("left_site"), py::arg("right_site"), py::arg("point"));

  m.def(
      "point_point_point_circle_exists",
      [](const SiteEvent& first_site, const SiteEvent& second_site,
         const SiteEvent& third_site) {
        static const Predicates::circle_existence_predicate<SiteEvent>
            predicate;
        return predicate.ppp(first_site, second_site, third_site);
      },
      py::arg("first_site"), py::arg("second_site"), py::arg("third_site"));

  m.def(
      "point_point_segment_circle_exists",
      [](const SiteEvent& first_site, const SiteEvent& second_site,
         const SiteEvent& third_site, int segment_index) {
        static const Predicates::circle_existence_predicate<SiteEvent>
            predicate;
        return predicate.pps(first_site, second_site, third_site,
                             segment_index);
      },
      py::arg("first_site"), py::arg("second_site"), py::arg("third_site"),
      py::arg("segment_index"));

  m.def(
      "point_segment_horizontal_goes_through_right_arc_first",
      [](const SiteEvent& left_site, const SiteEvent& right_site,
         const Point& point, bool reverse_order) {
        static const Predicates::distance_predicate<SiteEvent> comparator;
        return comparator.ps(left_site, right_site, point, reverse_order);
      },
      py::arg("left_site"), py::arg("right_site"), py::arg("point"),
      py::arg("reverse_order"));

  m.def(
      "point_segment_segment_circle_exists",
      [](const SiteEvent& first_site, const SiteEvent& second_site,
         const SiteEvent& third_site, int point_index) {
        static const Predicates::circle_existence_predicate<SiteEvent>
            predicate;
        return predicate.pss(first_site, second_site, third_site, point_index);
      },
      py::arg("first_site"), py::arg("second_site"), py::arg("third_site"),
      py::arg("point_index"));

  m.def(
      "recompute_point_point_point_circle_event",
      [](CircleEvent& circle_event, const SiteEvent& first_site,
         const SiteEvent& second_site, const SiteEvent& third_site,
         bool recompute_center_x, bool recompute_center_y,
         bool recompute_lower_x) {
        static Predicates::mp_circle_formation_functor<SiteEvent, CircleEvent>
            functor;
        functor.ppp(first_site, second_site, third_site, circle_event,
                    recompute_center_x, recompute_center_y, recompute_lower_x);
      },
      py::arg("circle_event"), py::arg("first_site"), py::arg("second_site"),
      py::arg("third_site"), py::arg("recompute_center_x") = true,
      py::arg("recompute_center_y") = true,
      py::arg("recompute_lower_x") = true);

  m.def(
      "recompute_point_point_segment_circle_event",
      [](CircleEvent& circle_event, const SiteEvent& first_site,
         const SiteEvent& second_site, const SiteEvent& third_site,
         int segment_index, bool recompute_center_x, bool recompute_center_y,
         bool recompute_lower_x) {
        static Predicates::mp_circle_formation_functor<SiteEvent, CircleEvent>
            functor;
        functor.pps(first_site, second_site, third_site, segment_index,
                    circle_event, recompute_center_x, recompute_center_y,
                    recompute_lower_x);
      },
      py::arg("circle_event"), py::arg("first_site"), py::arg("second_site"),
      py::arg("third_site"), py::arg("segment_index"),
      py::arg("recompute_center_x") = true,
      py::arg("recompute_center_y") = true,
      py::arg("recompute_lower_x") = true);

  m.def(
      "recompute_point_segment_segment_circle_event",
      [](CircleEvent& circle_event, const SiteEvent& first_site,
         const SiteEvent& second_site, const SiteEvent& third_site,
         int point_index, bool recompute_center_x, bool recompute_center_y,
         bool recompute_lower_x) {
        static Predicates::mp_circle_formation_functor<SiteEvent, CircleEvent>
            functor;
        functor.pss(first_site, second_site, third_site, point_index,
                    circle_event, recompute_center_x, recompute_center_y,
                    recompute_lower_x);
      },
      py::arg("circle_event"), py::arg("first_site"), py::arg("second_site"),
      py::arg("third_site"), py::arg("point_index"),
      py::arg("recompute_center_x") = true,
      py::arg("recompute_center_y") = true,
      py::arg("recompute_lower_x") = true);

  m.def(
      "recompute_segment_segment_segment_circle_event",
      [](CircleEvent& circle_event, const SiteEvent& first_site,
         const SiteEvent& second_site, const SiteEvent& third_site,
         bool recompute_center_x, bool recompute_center_y,
         bool recompute_lower_x) {
        static Predicates::mp_circle_formation_functor<SiteEvent, CircleEvent>
            functor;
        functor.sss(first_site, second_site, third_site, circle_event,
                    recompute_center_x, recompute_center_y, recompute_lower_x);
      },
      py::arg("circle_event"), py::arg("first_site"), py::arg("second_site"),
      py::arg("third_site"), py::arg("recompute_center_x") = true,
      py::arg("recompute_center_y") = true,
      py::arg("recompute_lower_x") = true);

  m.def("robust_cross_product", &Predicates::robust_cross_product,
        py::arg("first_dx"), py::arg("first_dy"), py::arg("second_dx"),
        py::arg("second_dy"));

  m.def(
      "robust_product_with_sqrt",
      [](BigInt& left, BigInt& right) {
        RobustSumExpression expression;
        return expression.eval1(&left, &right);
      },
      py::arg("left"), py::arg("right"));

  m.def(
      "robust_sum_of_products_with_sqrt_pairs",
      [](std::array<BigInt, 2>& left, std::array<BigInt, 2>& right) {
        RobustSumExpression expression;
        return expression.eval2(left.data(), right.data());
      },
      py::arg("left"), py::arg("right"));

  m.def(
      "robust_sum_of_products_with_sqrt_triplets",
      [](std::array<BigInt, 3>& left, std::array<BigInt, 3>& right) {
        RobustSumExpression expression;
        return expression.eval3(left.data(), right.data());
      },
      py::arg("left"), py::arg("right"));

  m.def(
      "robust_sum_of_products_with_sqrt_quadruplets",
      [](std::array<BigInt, 4>& left, std::array<BigInt, 4>& right) {
        RobustSumExpression expression;
        return expression.eval4(left.data(), right.data());
      },
      py::arg("left"), py::arg("right"));

  m.def(
      "segment_segment_horizontal_goes_through_right_arc_first",
      [](const SiteEvent& left_site, const SiteEvent& right_site,
         const Point& point) {
        static const Predicates::distance_predicate<SiteEvent> comparator;
        return comparator.ss(left_site, right_site, point);
      },
      py::arg("left_site"), py::arg("right_site"), py::arg("point"));

  m.def(
      "segment_segment_segment_circle_exists",
      [](const SiteEvent& first_site, const SiteEvent& second_site,
         const SiteEvent& third_site) {
        static const Predicates::circle_existence_predicate<SiteEvent>
            predicate;
        return predicate.sss(first_site, second_site, third_site);
      },
      py::arg("first_site"), py::arg("second_site"), py::arg("third_site"));

  m.def("to_first_point_segment_segment_quadruplets_expression",
        [](std::array<BigInt, 4> left, std::array<BigInt, 4> right) {
          static Predicates::mp_circle_formation_functor<SiteEvent, CircleEvent>
              functor;
          return functor.sqrt_expr_evaluator_pss3<BigInt, BigFloat>(
              left.data(), right.data());
        });

  m.def(
      "to_orientation",
      [](const Point& vertex, const Point& first_ray_point,
         const Point& second_ray_point) {
        return Predicates::ot::eval(vertex, first_ray_point, second_ray_point);
      },
      py::arg("vertex"), py::arg("first_ray_point"),
      py::arg("second_ray_point"));

  m.def("to_second_point_segment_segment_quadruplets_expression",
        [](std::array<BigInt, 4> left, std::array<BigInt, 4> right) {
          static Predicates::mp_circle_formation_functor<SiteEvent, CircleEvent>
              functor;
          return functor.sqrt_expr_evaluator_pss4<BigInt, BigFloat>(
              left.data(), right.data());
        });
}
