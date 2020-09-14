#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <sstream>
#include <stdexcept>

#include "voronoi.hpp"

namespace py = pybind11;

#define MODULE_NAME _voronoi
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#define CELL_NAME "Cell"
#define EDGE_NAME "Edge"
#define POINT_NAME "Point"
#define SEGMENT_NAME "Segment"
#define VERTEX_NAME "Vertex"
#define VORONOI_DIAGRAM_NAME "VoronoiDiagram"
#define VORONOI_EDGE_NAME "VoronoiEdge"
#define VORONOI_VERTEX_NAME "VoronoiVertex"

using coordinate_t = int;
using VoronoiEdge = voronoi_edge<double>;
using VoronoiVertex = voronoi_vertex<double>;

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

static std::ostream& operator<<(std::ostream& stream, const c_Edge& edge) {
  return stream << C_STR(MODULE_NAME) "." EDGE_NAME "(" << edge.start << ", "
                << edge.end << ", " << bool_repr(edge.isPrimary) << ", "
                << bool_repr(edge.isLinear) << ", " << edge.cell << ", "
                << edge.twin << ")";
}

static std::ostream& operator<<(std::ostream& stream, const c_Cell& cell) {
  stream << C_STR(MODULE_NAME) "." CELL_NAME "(" << cell.cell_identifier << ", "
         << cell.site << ", " << bool_repr(cell.contains_point) << ", "
         << bool_repr(cell.contains_segment) << ", " << bool_repr(cell.is_open)
         << ", " << bool_repr(cell.is_degenerate) << ", ";
  write_sequence(stream, cell.vertices);
  stream << ", ";
  write_sequence(stream, cell.edges);
  return stream << ", " << cell.source_category << ")";
}

static std::ostream& operator<<(std::ostream& stream, const Point& point) {
  return stream << C_STR(MODULE_NAME) "." POINT_NAME "(" << point.X << ", "
                << point.Y << ")";
}

static std::ostream& operator<<(std::ostream& stream, const Segment& segment) {
  return stream << C_STR(MODULE_NAME) "." SEGMENT_NAME "(" << segment.p0 << ", "
                << segment.p1 << ")";
}

static std::ostream& operator<<(std::ostream& stream, const c_Vertex& vertex) {
  return stream << C_STR(MODULE_NAME) "." VERTEX_NAME "(" << vertex.X << ", "
                << vertex.Y << ")";
}

static bool operator==(const c_Cell& left, const c_Cell& right) {
  return left.cell_identifier == right.cell_identifier &&
         left.site == right.site &&
         left.contains_point == right.contains_point &&
         left.contains_segment == right.contains_segment &&
         left.is_open == right.is_open &&
         left.is_degenerate == right.is_degenerate &&
         left.source_category == right.source_category &&
         left.vertices == right.vertices && left.edges == right.edges;
}

static bool operator==(const c_Edge& left, const c_Edge& right) {
  return left.start == right.start && left.end == right.end &&
         left.isPrimary == right.isPrimary && left.isLinear == right.isLinear &&
         left.cell == right.cell && left.twin == right.twin;
}

static bool operator==(const Point& left, const Point& right) {
  return left.X == right.X && left.Y == right.Y;
}

static bool operator==(const Segment& left, const Segment& right) {
  return left.p0 == right.p0 && left.p1 == right.p1;
}

static bool operator==(const c_Vertex& left, const c_Vertex& right) {
  return left.X == right.X && left.Y == right.Y;
}

namespace boost {
namespace polygon {
static std::ostream& operator<<(std::ostream& stream,
                                const VoronoiVertex& vertex) {
  return stream << C_STR(MODULE_NAME) "." VORONOI_VERTEX_NAME "(" << vertex.x()
                << ", " << vertex.y() << ")";
}

static bool operator==(const VoronoiVertex& left, const VoronoiVertex& right) {
  return left.x() == right.x() && left.y() == right.y();
}
}  // namespace polygon
}  // namespace boost

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(Python binding of Voxel8/pyvoronoi library.)pbdoc";

  py::class_<c_Cell>(m, CELL_NAME)
      .def(py::init([](std::size_t index, std::size_t site, bool contains_point,
                       bool contains_segment, bool is_open, bool is_degenerate,
                       const std::vector<long long>& vertices_indices,
                       const std::vector<long long>& edges_indices,
                       int source_category) {
             c_Cell result{index,          site,
                           contains_point, contains_segment,
                           is_open,        source_category};
             result.is_degenerate = is_degenerate;
             result.vertices = vertices_indices;
             result.edges = edges_indices;
             return result;
           }),
           py::arg("index"), py::arg("site"), py::arg("contains_point"),
           py::arg("contains_segment"), py::arg("is_open"),
           py::arg("is_degenerate"), py::arg("vertices_indices"),
           py::arg("edges_indices"), py::arg("source_category"))
      .def("__repr__", repr<c_Cell>)
      .def(py::self == py::self)
      .def_readonly("index", &c_Cell::cell_identifier)
      .def_readonly("contains_point", &c_Cell::contains_point)
      .def_readonly("contains_segment", &c_Cell::contains_segment)
      .def_readonly("edges_indices", &c_Cell::edges)
      .def_readonly("is_degenerate", &c_Cell::is_degenerate)
      .def_readonly("is_open", &c_Cell::is_open)
      .def_readonly("site", &c_Cell::site)
      .def_readonly("source_category", &c_Cell::source_category)
      .def_readonly("vertices_indices", &c_Cell::vertices);

  py::class_<c_Edge>(m, EDGE_NAME)
      .def(py::init<long long, long long, bool, bool, long long, long long>(),
           py::arg("start_index"), py::arg("end_index"), py::arg("is_primary"),
           py::arg("is_linear"), py::arg("cell_index"), py::arg("twin_index"))
      .def("__repr__", repr<c_Edge>)
      .def(py::self == py::self)
      .def_readonly("start_index", &c_Edge::start)
      .def_readonly("end_index", &c_Edge::end)
      .def_readonly("is_primary", &c_Edge::isPrimary)
      .def_readonly("is_linear", &c_Edge::isLinear)
      .def_readonly("cell_index", &c_Edge::cell)
      .def_readonly("twin_index", &c_Edge::twin);

  py::class_<Point>(m, POINT_NAME)
      .def(py::init<coordinate_t, coordinate_t>(), py::arg("x"), py::arg("y"))
      .def("__repr__", repr<Point>)
      .def(py::self == py::self)
      .def_readonly("x", &Point::X)
      .def_readonly("y", &Point::Y);

  py::class_<Segment>(m, SEGMENT_NAME)
      .def(py::init<Point, Point>(), py::arg("start"), py::arg("end"))
      .def("__repr__", repr<Segment>)
      .def(py::self == py::self)
      .def_readonly("start", &Segment::p0)
      .def_readonly("end", &Segment::p1);

  py::class_<c_Vertex>(m, VERTEX_NAME)
      .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
      .def("__repr__", repr<c_Vertex>)
      .def(py::self == py::self)
      .def_readonly("x", &c_Vertex::X)
      .def_readonly("y", &c_Vertex::Y);

  py::class_<VoronoiDiagram>(m, VORONOI_DIAGRAM_NAME)
      .def(py::init<>())
      .def("add_point", &VoronoiDiagram::AddPoint)
      .def("add_segment", &VoronoiDiagram::AddSegment)
      .def("construct",
           [](VoronoiDiagram& self) {
             self.Construct();
             self.MapVertexIndexes();
             self.MapEdgeIndexes();
             self.MapCellIndexes();
           })
      .def_property_readonly("cells",
                             [](VoronoiDiagram& self) {
                               std::vector<c_Cell> cells;
                               for (std::size_t index = 0;
                                    index < self.CountCells(); ++index)
                                 cells.push_back(self.GetCell(index));
                               return cells;
                             })
      .def_property_readonly("edges",
                             [](VoronoiDiagram& self) {
                               std::vector<c_Edge> edges;
                               for (std::size_t index = 0;
                                    index < self.CountEdges(); ++index)
                                 edges.push_back(self.GetEdge(index));
                               return edges;
                             })
      .def_property_readonly("points", &VoronoiDiagram::GetPoints)
      .def_property_readonly("segments", &VoronoiDiagram::GetSegments)
      .def_property_readonly("vertices", [](VoronoiDiagram& self) {
        std::vector<c_Vertex> vertices;
        for (std::size_t index = 0; index < self.CountVertices(); ++index)
          vertices.push_back(self.GetVertex(index));
        return vertices;
      });

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

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
